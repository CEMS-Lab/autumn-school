// Local-page checks for seven vector diagrams, with external requests blocked.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const {pathToFileURL} = require('url');
const {chromium} = require('playwright');

(async () => {
  const root = path.resolve(process.argv[2] || 'book');
  const baseURL = process.env.COURSE_BASE_URL;
  const out = path.resolve(process.argv[3] || 'reviews/flowcharts');
  fs.mkdirSync(out, {recursive:true});
  const browser = await chromium.launch({headless:true,
    ...(process.env.BROWSER_EXECUTABLE ? {executablePath:process.env.BROWSER_EXECUTABLE} : {})});
  const lessons = ['index', '01_crack_representations', '03_staggered_solution',
    '04_fem_to_tensors', '05_differentiation_and_inverse',
    '05a_backpropagation_step_by_step', '06_learning_adapter'];
  const results = [];
  try {
    for (const width of [1440,390]) {
      const context = await browser.newContext({viewport:{width,height:1000},offline:!baseURL});
      await context.route(/^https?:/, route =>
        baseURL && new URL(route.request().url()).origin === new URL(baseURL).origin
          ? route.continue() : route.abort());
      for (const name of lessons) {
        const page = await context.newPage();
        const errors = [], failed = [];
        page.on('pageerror',e=>errors.push(e.message));
        page.on('requestfailed',r=>failed.push(r.url()));
        await page.goto(baseURL ? new URL(name+'.html', baseURL).href
          : pathToFileURL(path.join(root,name+'.html')).href);
        await page.evaluate(async()=>{
          if(window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
          await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));
          await document.fonts.ready;
        });
        await page.waitForLoadState('networkidle');
        const figure = page.locator('figure').first();
        const img = figure.locator('img');
        assert.ok((await img.getAttribute('src')).endsWith('.svg'));
        assert.ok((await img.getAttribute('alt')).length > 50);
        assert.ok(await img.evaluate(i=>i.complete && i.naturalWidth>0));
        assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
        await figure.scrollIntoViewIfNeeded();
        await page.screenshot({path:path.join(out, name+'-'+width+'.png')});
        const link = figure.locator('a.image-reference');
        await link.focus();
        await page.keyboard.press('Enter');
        await page.waitForURL(/\.svg$/);
        await page.evaluate(()=>document.fonts.ready);
        const svg = await page.locator('svg').evaluate(el=>({
          text:el.querySelectorAll('text').length,
          embedded:el.innerHTML.includes('data:font/') || el.innerHTML.includes('data:application/'),
        }));
        assert.ok(svg.text>10 && svg.embedded, 'Live text and embedded fonts required');
        if(name==='05a_backpropagation_step_by_step' && width===1440)
          await page.screenshot({path:path.join(out,'backprop-vector.png')});
        assert.deepEqual(errors,[]); assert.deepEqual(failed,[]);
        results.push({name,width,vector:true,alt:true,keyboardEnlarge:true,svg});
        await page.close();
      }
      await context.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(out,'report.json'), JSON.stringify({passed:true,results},null,2)+'\n');
  console.log(JSON.stringify({passed:true,pageViewportChecks:results.length}));
})().catch(e=>{console.error(e);process.exit(1);});
