const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const {pathToFileURL, fileURLToPath} = require('url');
const {chromium} = require('playwright');
const {PNG} = require('pngjs');

(async () => {
  const root = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3]);
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true,
    executablePath:'/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'});
  const records = [];
  try {
    for (const width of [1440,390]) {
      const context = await browser.newContext({viewport:{width,height:1000},offline:true,
        reducedMotion:'reduce'});
      const page = await context.newPage();
      const pageName = process.argv[4] || '08_visual_lab';
      const expectedVideos = Number(process.argv[5] || 3);
      await page.goto(pathToFileURL(path.join(root,pageName+'.html')).href);
      await page.evaluate(async()=>{if(window.MathJax?.startup?.promise) await window.MathJax.startup.promise;});
      const videos = page.locator('video');
      assert.equal(await videos.count(),expectedVideos);
      for(let i=0;i<expectedVideos;i++) {
        const video = videos.nth(i);
        const contract = await video.evaluate(v=>({src:v.src,poster:v.poster,controls:v.controls,
          autoplay:v.autoplay,preload:v.preload,paused:v.paused,name:v.dataset.visualFilm}));
        assert.ok(contract.controls && contract.paused && !contract.autoplay);
        assert.equal(contract.preload,'none');
        assert.ok(fs.existsSync(fileURLToPath(contract.src)));
        assert.ok(fs.existsSync(fileURLToPath(contract.poster)));
        await video.scrollIntoViewIfNeeded();
        const media = await video.evaluate(async v=>{
          await new Promise((resolve,reject)=>{
            v.addEventListener('loadeddata',resolve,{once:true});
            v.addEventListener('error',()=>reject(new Error('Video decode failed')),{once:true});
            v.load();
          });
          return {duration:v.duration,width:v.videoWidth,height:v.videoHeight};
        });
        assert.ok(media.duration>0 && media.width>0 && media.height>0);
        await video.evaluate(async v=>{
          await v.play();
          await new Promise(resolve=>v.requestVideoFrameCallback(resolve));
          v.pause();
          await new Promise(resolve=>{v.addEventListener('seeked',resolve,{once:true});v.currentTime=.01;});
          await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
        });
        // File URLs play normally but taint a DOM canvas; inspect native screenshots.
        const pixels = async()=>PNG.sync.read(await video.screenshot());
        const first = await pixels();
        await video.screenshot({path:path.join(output,`${width}-${i}-first.png`)});
        await video.evaluate(async v=>{await v.play();});
        await page.waitForTimeout(450);
        const progressed=await video.evaluate(v=>{v.pause();return v.currentTime;});
        assert.ok(progressed>0);
        await video.evaluate(async v=>{
          await new Promise(resolve=>{v.addEventListener('seeked',resolve,{once:true});v.currentTime=v.duration-.05;});
        });
        const last=await pixels();
        assert.equal(first.width,last.width);assert.equal(first.height,last.height);
        let change=0,count=0;
        // Exclude the native playback-control strip from the pixel comparison.
        for(let y=0;y<Math.floor(first.height*.8);y++) for(let x=0;x<first.width;x++) {
          const k=(y*first.width+x)*4;
          for(let channel=0;channel<3;channel++){change+=Math.abs(first.data[k+channel]-last.data[k+channel]);count++;}
        }
        const meanChange=change/count;
        assert.ok(meanChange>.05, 'Decoded movie did not change');
        await video.screenshot({path:path.join(output,`${width}-${i}-last.png`)});
        records.push({viewport:width,...contract,...media,meanPixelChange:meanChange,playbackAdvanced:progressed});
      }
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
      await context.close();
    }
    fs.writeFileSync(path.join(output,'video_report.json'),JSON.stringify({passed:true,records},null,2));
    console.log(JSON.stringify({passed:true,videoViewportChecks:records.length}));
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
