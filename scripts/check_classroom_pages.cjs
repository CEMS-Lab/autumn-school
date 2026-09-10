// Browser-only classroom QA. No notebook execution or external network access.
// Run with NODE_PATH, BROWSER_EXECUTABLE, and optional COURSE_BASE_URL configured.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const {chromium} = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const BASE = process.env.COURSE_BASE_URL || 'http://127.0.0.1:8767/book/';
const origin = new URL(BASE).origin;
assert.ok(['127.0.0.1', 'localhost', '[::1]'].includes(new URL(BASE).hostname),
  'Run this local delivery check against a loopback HTTP server.');
const OUT = path.resolve(process.argv[2] || path.join(ROOT, 'reviews/classroom-20260910'));
const REPORT = path.join(ROOT, 'evidence/classroom_browser_20260910.json');
const NAMES = [
  '00_why_average_predictions_can_fail', '01_phast_tiny_evolving_fracture',
  '02_degradation_autograd', '03_tiny_derivative_inverse_toy',
  '04_train_save_reload_adapter', '05_hybrid_reference_correction',
];

function relative(p) { return path.relative(ROOT, p).split(path.sep).join('/'); }

async function settled(page) {
  await page.evaluate(async () => {
    if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
    await Promise.all([...document.images].map(img => img.decode().catch(() => {})));
    await document.fonts.ready;
  });
  await page.waitForLoadState('networkidle');
}

async function documentChecks(page, result) {
  const state = await page.evaluate(() => ({
    width: innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    mathContainers: document.querySelectorAll('article mjx-container').length,
    mathErrors: [...document.querySelectorAll('mjx-merror, .MathJax_Error')].map(el => el.textContent),
    unrenderedMath: [...document.querySelectorAll('article .math')]
      .filter(el => !el.querySelector('mjx-container')).map(el => el.textContent.slice(0, 140)),
    brokenImages: [...document.images].filter(img => !img.complete || !img.naturalWidth)
      .map(img => img.getAttribute('src')),
    theme: document.documentElement.dataset.theme,
    scrollableMath: [...document.querySelectorAll('article mjx-container[display]')]
      .filter(el => el.scrollWidth > el.clientWidth + 1).length,
  }));
  result.document = state;
  assert.ok(state.scrollWidth <= state.width + 1, 'Horizontal page overflow');
  assert.deepEqual(state.mathErrors, [], 'MathJax parsing errors');
  assert.deepEqual(state.unrenderedMath, [], 'Unrendered math delimiters');
  assert.deepEqual(state.brokenImages, [], 'Broken image assets');
  assert.equal(state.theme, 'dark', 'Initial dark theme');
}

async function capture(page, locator, stem, result) {
  if (locator) await locator.scrollIntoViewIfNeeded();
  else await page.evaluate(() => scrollTo(0, 0));
  const filename = path.join(OUT, stem + '.png');
  await page.screenshot({path: filename});
  result.screenshots.push(relative(filename));
}

async function checkLinks(page, result, name) {
  const badges = page.locator('article .badge-row');
  assert.equal(await badges.count(), 1, 'Exactly one action badge group');
  const expected = [
    ['practice', 'a.badge-link[href*="/notebooks/study/"]', 'notebook'],
    ['solutions', 'a.badge-link[href*="/notebooks/solutions/"]', 'notebook'],
    ['setup', 'a.badge-link[href$="/SETUP.md"]', 'markdown'],
  ];
  result.actions = {};
  for (const [label, selector, kind] of expected) {
    const link = badges.locator(selector);
    assert.equal(await link.count(), 1, `${label} action link`);
    const url = await link.evaluate(el => el.href);
    assert.equal(new URL(url).origin, origin, `${label} remains local`);
    const response = await page.request.get(url);
    assert.equal(response.status(), 200, `${label} HTTP response`);
    if (kind === 'notebook') {
      const notebook = await response.json();
      assert.equal(notebook.nbformat, 4);
      assert.ok(notebook.cells.some(c => c.cell_type === 'code'));
    } else assert.match(await response.text(), /Python|environment/i);
    result.actions[label] = {url, httpStatus: response.status()};
  }
  const colab = badges.locator('a[href^="https://colab.research.google.com/"]');
  assert.equal(await colab.count(), 1, 'One Colab launch link');
  const colabHref = await colab.getAttribute('href');
  assert.ok(colabHref.endsWith('/notebooks/study/' + name + '.ipynb'));
  result.actions.colab = {href: colabHref, checked: 'target only; no external request or runtime launch'};
}

(async () => {
  fs.mkdirSync(OUT, {recursive: true});
  const browser = await chromium.launch({headless: true,
    ...(process.env.BROWSER_EXECUTABLE ? {executablePath: process.env.BROWSER_EXECUTABLE} : {})});
  const report = {date: '2026-09-10', baseURL: BASE,
    scope: 'Local desktop/mobile HTML, math, assets, downloads, keyboard answers, and screenshots; no numerical or Colab execution.',
    screenshotsDirectory: relative(OUT), passed: true, results: []};
  try {
    for (const width of [1440, 390]) {
      const context = await browser.newContext({viewport: {width, height: 1000}, colorScheme: 'dark'});
      for (const name of ['index', ...NAMES]) {
        const result = {name, width, passed: false, screenshots: [], pageErrors: [],
          localFailedRequests: [], localHttpErrors: [], blockedExternalRequests: []};
        report.results.push(result);
        const page = await context.newPage();
        await page.route(/^https?:/, route => {
          if (new URL(route.request().url()).origin === origin) return route.continue();
          result.blockedExternalRequests.push(route.request().url());
          return route.abort();
        });
        page.on('pageerror', error => result.pageErrors.push(error.message));
        page.on('requestfailed', request => {
          if (new URL(request.url()).origin === origin)
            result.localFailedRequests.push({url: request.url(), error: request.failure()?.errorText});
        });
        page.on('response', response => {
          if (new URL(response.url()).origin === origin && response.status() >= 400)
            result.localHttpErrors.push({url: response.url(), status: response.status()});
        });
        try {
          const url = new URL(name === 'index' ? 'index.html' : 'labs/' + name + '.html', BASE).href;
          assert.equal((await page.goto(url)).status(), 200);
          await settled(page);
          await documentChecks(page, result);
          await capture(page, null, `${name}-${width}-opening`, result);
          if (name === 'index') {
            assert.equal(await page.locator('#fig-course-map, img[src*="00_course_map"]').count(), 0);
            for (const lab of NAMES)
              assert.ok(await page.locator(`article a[href*="labs/${lab}.html"]`).count());
            result.index = {oldTimetableRemoved: true, allSixLabsLinked: true};
          } else {
            assert.equal(await page.locator('article h2').filter({hasText: /^Key takeaways/}).count(), 1);
            await checkLinks(page, result, name);
            const displayed = page.locator('article div.math:visible');
            const displayMath = (await displayed.count() ? displayed : page.locator('article .math:visible')).first();
            assert.ok(await displayMath.count(), 'Visible mathematical expression');
            await capture(page, displayMath, `${name}-${width}-math`, result);
            const figure = page.locator('article .cell_output img').first();
            assert.ok(await figure.count(), 'Retained computational figure');
            await capture(page, figure, `${name}-${width}-figure`, result);
            const enlarge = figure.locator('xpath=parent::a');
            assert.equal(await enlarge.count(), 1, 'Figure has an enlargement link');
            const imageURL = await figure.evaluate(el => el.src);
            assert.equal(await enlarge.evaluate(el => el.href), imageURL);
            assert.match(await enlarge.getAttribute('aria-label'), /^Open full-size figure:/);
            const articleURL = page.url();
            await enlarge.focus();
            await Promise.all([page.waitForURL(imageURL), page.keyboard.press('Enter')]);
            assert.equal((await page.request.get(imageURL)).status(), 200);
            result.figureEnlargement = {keyboardEnterOpens: true, url: imageURL};
            await page.goBack();
            await page.waitForURL(articleURL);
            await settled(page);
            const answers = page.locator('article details.worked-answer');
            assert.equal(await answers.count(), 4, 'Two hints and two worked solutions');
            result.keyboardAnswers = [];
            for (let i = 0; i < 4; i++) {
              const answer = answers.nth(i);
              const summary = answer.locator(':scope > summary');
              assert.equal(await answer.evaluate(el => el.open), false);
              await summary.focus();
              await page.keyboard.press('Enter');
              assert.equal(await answer.evaluate(el => el.open), true, 'Enter opens answer');
              result.keyboardAnswers.push({title: await summary.innerText(), opensWithEnter: true});
              await page.keyboard.press('Space');
              assert.equal(await answer.evaluate(el => el.open), false, 'Space closes answer');
            }
            const showAll = page.getByRole('button', {name: 'Show all hints and solutions', exact: true});
            await showAll.focus();
            await page.keyboard.press('Enter');
            assert.ok(await answers.evaluateAll(elements => elements.every(el => el.open)));
            await settled(page);
            await documentChecks(page, result);
            result.keyboardMathScroll = [];
            const mathRegions = page.locator('article mjx-container[display]');
            for (let i = 0; i < await mathRegions.count(); i++) {
              const math = mathRegions.nth(i);
              const dimensions = await math.evaluate(el => ({client: el.clientWidth, scroll: el.scrollWidth}));
              if (dimensions.client < 1 || dimensions.scroll <= dimensions.client + 1) continue;
              assert.equal(await math.evaluate(el => el.tabIndex), 0, 'Scrollable equation is keyboard focusable');
              await math.focus();
              await math.evaluate(el => { el.scrollLeft = 0; });
              await page.keyboard.press('ArrowRight');
              await page.waitForFunction(el => el.scrollLeft > 0, await math.elementHandle(), {timeout: 1500});
              result.keyboardMathScroll.push({...dimensions, arrowRightScrolls: true});
              await math.evaluate(el => { el.scrollLeft = 0; });
            }
            // Finish the browser's animated keyboard scroll before resetting the
            // equations for screenshots of their leftmost, unfocused state.
            await page.waitForTimeout(200);
            await page.evaluate(() => {
              document.activeElement?.blur();
              document.querySelectorAll('article mjx-container[display]').forEach(el => {
                el.scrollTo({left: 0, behavior: 'instant'});
              });
            });
            await capture(page, answers.nth(1), `${name}-${width}-worked-solution`, result);
            result.takeaways = 1;
            result.showAllKeyboard = true;
          }
          assert.deepEqual(result.pageErrors, []);
          assert.deepEqual(result.localFailedRequests, []);
          assert.deepEqual(result.localHttpErrors, []);
          assert.deepEqual(result.blockedExternalRequests, [], 'All required runtime assets are local');
          result.passed = true;
        } catch (error) {
          report.passed = false;
          result.failure = error.message;
          await capture(page, null, `${name}-${width}-failure`, result).catch(() => {});
          console.error(`${name} ${width}: ${error.message}`);
        } finally { await page.close(); }
        fs.writeFileSync(REPORT, JSON.stringify(report, null, 2) + '\n');
      }
      await context.close();
    }
  } finally { await browser.close(); }
  report.pageViewportChecks = report.results.length;
  report.manualVisualReview = 'Screenshot capture complete; record human/model visual inspection in the independent review report.';
  report.manualVisualReviewReport = 'evidence/notebook_delivery_review_20260910.md';
  fs.writeFileSync(REPORT, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({passed: report.passed, checks: report.results.length, report: relative(REPORT)}));
  process.exitCode = report.passed ? 0 : 1;
})().catch(error => { console.error(error); process.exitCode = 1; });
