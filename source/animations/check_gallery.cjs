const {chromium} = require("playwright");
const fs = require("fs");
const path = require("path");
const {pathToFileURL} = require("url");
(async () => {
  const root = path.resolve(__dirname, "../..");
  const gallery = path.join(root, "assets/animations/index.html");
  const out = path.join(root, ".build/animation-review");
  fs.mkdirSync(out, {recursive:true});
  const browser = await chromium.launch({
    executablePath:"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    headless:true, args:["--allow-file-access-from-files","--autoplay-policy=no-user-gesture-required"]
  });
  const results = [];
  for (const width of [1440,390]) {
    const page = await browser.newPage({viewport:{width,height:1000}});
    const errors=[], failures=[], mediaSeekCancellations=[], external=[];
    page.on("pageerror", e=>errors.push(e.message));
    page.on("requestfailed",r=>{
      const failure={url:r.url(),failure:r.failure()};
      // Media range requests can be cancelled when playback/seek changes.
      // Require successful decoded playback and seek below, and report these.
      if(r.url().endsWith(".mp4") && r.failure()?.errorText==="net::ERR_ABORTED")
        mediaSeekCancellations.push(failure);
      else failures.push(failure);
    });
    page.on("request",r=>{if(/^https?:/.test(r.url())) external.push(r.url())});
    await page.goto(pathToFileURL(gallery).href);
    await page.waitForFunction(()=>Array.from(document.querySelectorAll("video")).every(v=>Number.isFinite(v.duration)),null,{timeout:20000});
    const clips = [];
    for (let i=0; i<4; i++) {
      const video=page.locator("video").nth(i);
      await video.scrollIntoViewIfNeeded();
      const info=await video.evaluate(async v=>{
        v.muted=true;
        await v.play();
        await new Promise(resolve=>setTimeout(resolve,250));
        v.pause();
        const advanced=v.currentTime>0;
        v.currentTime=v.duration/2;
        await new Promise(resolve=>v.addEventListener("seeked",resolve,{once:true}));
        return {duration:v.duration,width:v.videoWidth,height:v.videoHeight,
          currentTime:v.currentTime,advanced,readyState:v.readyState,error:v.error?.message || null};
      });
      if(!info.advanced || info.error || info.width!==1280) throw Error(JSON.stringify(info));
      clips.push(info);
    }
    // Test native, keyboard-operated worked answers.
    const answer = page.locator("summary").first();
    await answer.focus();
    await page.keyboard.press("Enter");
    if(!await answer.evaluate(el=>el.parentElement.open)) throw Error("Keyboard answer did not open");
    const overflow = await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    const missingImages=await page.locator("img").evaluateAll(imgs=>imgs.filter(i=>!i.complete||i.naturalWidth===0).length);
    if(overflow||missingImages||errors.length||failures.length||external.length)
      throw Error(JSON.stringify({width,overflow,missingImages,errors,failures,external}));
    await page.screenshot({path:path.join(out,"gallery-"+width+".png"),fullPage:true});
    await page.emulateMedia({media:"print"});
    const printPosters=await page.locator(".print-poster").evaluateAll(imgs=>imgs.filter(i=>getComputedStyle(i).display!=="none").length);
    if(printPosters!==4) throw Error("Print posters missing");
    results.push({width,clips,keyboardAnswer:true,overflow,missingImages,printPosters,externalRequests:external.length,errors,failures,mediaSeekCancellations});
    await page.close();
  }
  await browser.close();
  const result={passed:true,scope:"Offline gallery playback; not native PowerPoint or Colab",results};
  fs.writeFileSync(path.join(out,"browser.json"),JSON.stringify(result,null,2));
  process.stdout.write(JSON.stringify(result,null,2)+"\n");
})().catch(e=>{process.stderr.write(String(e.stack||e));process.exit(1)});
