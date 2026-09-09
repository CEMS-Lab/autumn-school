const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const {pathToFileURL}=require("url"),{chromium}=require("playwright"),{PNG}=require("pngjs");
(async()=>{
 const input=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]);
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"});
 const records=[];
 try{
  for(const width of [1280,390]){
   const page=await browser.newPage({viewport:{width,height:1000},offline:true,reducedMotion:"reduce"});
   const errors=[];page.on("pageerror",e=>errors.push(e.message));
   await page.goto(pathToFileURL(input).href);
   assert.equal(await page.locator(".walkthrough section[id]").count(),8);
   assert.ok(await page.locator(".walkthrough math").count()>=12);
   assert.equal(await page.locator("[data-guide-frame]").count(),2);
   assert.ok(await page.locator("[data-guide-frame]").evaluateAll(es=>es.every(e=>e.getAttribute("href").startsWith("data:image/png"))));
   const sizes=await page.locator("math").evaluateAll(es=>es.map(e=>({w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height})));
   assert.ok(sizes.every(s=>s.w>20&&s.h>15));
   for(const name of ["guide-setup","guide-history","guide-bounds","guide-reverse"]){
    await page.locator('.route a[href="#'+name+'"]').click();
    await page.locator("#"+name).screenshot({path:path.join(output,width+"-"+name+".png")});
   }
   const video=page.locator("#cycle-video");
   assert.ok(await video.evaluate(v=>v.paused&&v.controls&&!v.autoplay));
   await video.scrollIntoViewIfNeeded();
   const media=await video.evaluate(async v=>{
    await new Promise((resolve,reject)=>{v.addEventListener("loadeddata",resolve,{once:true});v.addEventListener("error",()=>reject(Error("Video decode failed")),{once:true});v.load();});
    return {duration:v.duration,width:v.videoWidth,height:v.videoHeight};
   });
   assert.ok(Math.abs(media.duration-40)<.2);
   await video.evaluate(async v=>{await v.play();await new Promise(r=>v.requestVideoFrameCallback(r));v.pause();});
   const first=PNG.sync.read(await video.screenshot({path:path.join(output,width+"-cycle-first.png")}));
   await video.evaluate(async v=>{const decoded=new Promise(r=>v.requestVideoFrameCallback(r));await new Promise(r=>{v.addEventListener("seeked",r,{once:true});v.currentTime=17.5;});await decoded;});
   const later=PNG.sync.read(await video.screenshot({path:path.join(output,width+"-cycle-history.png")}));
   let change=0,count=0;
   for(let y=0;y<first.height*.8;y++)for(let x=0;x<first.width;x++){
    const k=(y*first.width+x)*4;change+=Math.abs(first.data[k]-later.data[k]);count++;
   }
   assert.ok(change/count>.1);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   assert.deepEqual(errors,[]);
   records.push({width,equations:sizes.length,media,meanFrameChange:change/count});
   await page.close();
  }
  fs.writeFileSync(path.join(output,"report.json"),JSON.stringify({passed:true,records},null,2));
  console.log(JSON.stringify({passed:true,viewports:records.length}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
