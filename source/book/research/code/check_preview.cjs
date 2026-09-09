const fs = require("fs");
const path = require("path");
const assert = require("assert/strict");
const {pathToFileURL, fileURLToPath} = require("url");
const {chromium} = require("playwright");

(async () => {
  const root = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3]);
  fs.mkdirSync(output, {recursive:true});
  const names = ["index", "01_geometry", "02_observations", "03_derivatives",
    "04_recovery", "05_learning", "06_applications", "07_results",
    "notebooks/inverse_experiments"];
  const browser = await chromium.launch({headless:true,
    executablePath:"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"});
  const records = [];
  try {
    for (const width of [1440, 390]) {
      const context = await browser.newContext({viewport:{width,height:1000},offline:true});
      for (const name of names) {
        const slug = name.replaceAll("/", "-");
        const page = await context.newPage();
        const errors = [], failed = [];
        page.on("pageerror", err => errors.push(err.message));
        page.on("requestfailed", req => failed.push(req.url()));
        await page.goto(pathToFileURL(path.join(root,name+".html")).href);
        await page.evaluate(async () => {
          if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
          [...document.images].forEach(img => {img.loading="eager";});
          await Promise.all([...document.images].map(img => img.decode().catch(()=>{})));
        });
        const answers = page.locator(".worked-answer");
        if (await answers.count()) {
          const first = answers.first();
          assert.equal(await first.evaluate(el=>el.open), false);
          await first.locator("summary").focus();
          await page.keyboard.press("Enter");
          assert.equal(await first.evaluate(el=>el.open), true);
          await answers.evaluateAll(els => els.forEach(el=>{el.open=true;}));
        }
        const record = await page.evaluate(() => ({
          title:document.querySelector("h1")?.innerText,
          answers:document.querySelectorAll(".worked-answer").length,
          images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
          math:document.querySelectorAll("mjx-container").length,
          mathErrors:document.querySelectorAll("mjx-merror, [data-mjx-error]").length,
          scrollWidth:document.documentElement.scrollWidth,
          localLinks:[...document.querySelectorAll("a[href]")].map(a=>a.href).filter(s=>s.startsWith("file:"))
        }));
        for (const href of record.localLinks) {
          const u = new URL(href); u.hash="";
          assert.ok(fs.existsSync(fileURLToPath(u)), "Missing local link: "+href);
        }
        assert.deepEqual(record.images, [], name+" images");
        assert.equal(record.mathErrors, 0, name+" math");
        assert.ok(record.scrollWidth<=width+1, name+" horizontal overflow");
        assert.deepEqual(errors, [], name+" JS errors");
        assert.deepEqual(failed, [], name+" offline resources");
        if (name === "notebooks/inverse_experiments") {
          assert.equal(await page.locator(".cell_input").count(), 14);
          assert.equal(await page.locator(".cell_output img").count(), 7);
          await page.locator(".cell_output img").first().scrollIntoViewIfNeeded();
          await page.screenshot({path:path.join(output,"notebook-output-"+width+".png")});
        }
        await page.screenshot({path:path.join(output,slug+"-"+width+".png"),fullPage:true});
        const figure = page.locator("figure").first();
        if (await figure.count()) {
          await figure.scrollIntoViewIfNeeded();
          await page.screenshot({path:path.join(output,slug+"-figure-"+width+".png")});
        }
        delete record.localLinks;
        records.push({name,width,...record,errors,failed});
        await page.close();
      }
      await context.close();
    }
    const context = await browser.newContext({javaScriptEnabled:false,offline:true});
    const page = await context.newPage();
    await page.goto(pathToFileURL(path.join(root,"01_geometry.html")).href);
    assert.ok(await page.locator(".admonition.dropdown").first().isVisible());
    await context.close();
    fs.writeFileSync(path.join(output,"report.json"),JSON.stringify({passed:true,records},null,2));
    console.log(JSON.stringify({passed:true,pages:records.length,answers:records.reduce((n,r)=>n+r.answers,0)/2}));
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
