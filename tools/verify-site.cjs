/* Run with the bundled Node runtime. QA outputs stay inside main/qa. */
let playwright;
try { playwright = require('playwright'); }
catch { playwright = require('C:/Users/a/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'); }
const { chromium } = playwright;
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const base = process.env.DESIGNER_PREVIEW_URL || 'http://127.0.0.1:4173/';
const results = [];
const errors = [];
const failures = [];

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge', args: ['--disable-gpu'] });
  try {
    const context = await browser.newContext({ reducedMotion: 'reduce' });
    const page = await context.newPage();
    page.on('pageerror', e => errors.push(String(e)));
    page.on('response', r => { if (r.status() >= 400) failures.push(`${r.status()} ${r.url()}`); });
    for (const width of [1440, 1024, 768, 390, 320]) {
      await page.setViewportSize({ width, height: 960 });
      for (const file of ['index.html', 'privacy.html', 'terms.html']) {
        await page.goto(base + file);
        await page.evaluate(() => document.fonts.ready);
        await page.locator('footer').scrollIntoViewIfNeeded();
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForFunction(() => [...document.images].filter(i => !i.loading || i.loading !== 'lazy').every(i => i.complete));
        const info = await page.evaluate(() => ({
          width: innerWidth,
          scrollWidth: document.documentElement.scrollWidth,
          title: document.title,
          h1: document.querySelectorAll('h1').length,
          broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
          duplicateIds: [...document.querySelectorAll('[id]')].map(x => x.id).filter((id, i, ids) => ids.indexOf(id) !== i)
        }));
        assert(info.scrollWidth <= width, `Overflow in ${file} at ${width}: ${info.scrollWidth}`);
        assert.equal(info.h1, 1);
        assert.equal(info.broken.length, 0);
        assert.equal(info.duplicateIds.length, 0);
        results.push({ file, width, ...info });
        if ([1440, 768, 390].includes(width)) {
          await page.screenshot({ path: path.join(root, 'qa', `${file.replace('.html', '')}-${width}.png`), fullPage: true });
        }
      }
    }
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto(base);
    for (const policy of ['Privacy Policy', 'Terms of Use']) {
      const link = page.locator('#nav-links').getByRole('link', { name: `${policy} (opens in a new tab)`, exact: true });
      const [popup] = await Promise.all([page.waitForEvent('popup'), link.click()]);
      await popup.waitForLoadState();
      assert.equal(await popup.locator('h1').textContent(), policy);
      assert.equal(page.url(), base);
      await popup.close();
    }
    for (const id of ['mool', 'live-3d', 'layout', 'analysis', 'custom', 'release']) {
      assert.equal(await page.locator(`#${id}`).isVisible(), true);
    }
    results.push({ revision: 'Header policies open in new tabs; all six detailed capability sections are visible without tab interaction.' });
    await page.getByRole('tab', { name: '02 Live 3D' }).click();
    assert.equal(await page.locator('#panel-live').isVisible(), true);
    assert.equal(await page.locator('#panel-mool').isVisible(), false);
    await page.getByRole('tab', { name: '02 Live 3D' }).press('ArrowRight');
    assert.equal(await page.locator('#tab-layout').getAttribute('aria-selected'), 'true');
    await page.locator('#tab-layout').press('End');
    assert.equal(await page.locator('#panel-workspace').isVisible(), true);
    await page.locator('#tab-workspace').press('Home');
    assert.equal(await page.locator('#panel-mool').isVisible(), true);
    for (const tab of ['mool', 'live', 'layout', 'workspace']) {
      await page.locator(`#tab-${tab}`).click();
      await page.locator(`#panel-${tab} img`).evaluate(i => i.decode());
      assert.equal(await page.locator(`#panel-${tab}`).isVisible(), true);
    }
    const question = page.locator('.faq summary').first();
    await question.focus();
    await question.press('Enter');
    assert.equal(await question.evaluate(e => e.parentElement.open), true);
    await question.press('Enter');
    assert.equal(await question.evaluate(e => e.parentElement.open), false);
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(base);
    await page.getByRole('button', { name: 'Menu' }).click();
    assert.equal(await page.locator('#nav-links').isVisible(), true);
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#nav-links').isVisible(), false);
    assert.equal(await page.locator('.nav-toggle').evaluate(e => e === document.activeElement), true);
    await page.getByRole('button', { name: 'Menu' }).click();
    await page.locator('#nav-links a[href="#start"]').click();
    assert.equal(await page.locator('.nav-toggle').getAttribute('aria-expanded'), 'false');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'start');
    await page.goto(base);
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.activeElement.className), 'skip-link');
    await page.keyboard.press('Enter');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'main');
    results.push({ interactions: 'tabs, arrow/Home/End keys, FAQ keyboard, mobile menu, Escape focus return, section focus, skip link passed' });

    // A project-subpath URL catches root-relative links that break on GitHub Pages.
    for (const file of ['index.html', 'privacy.html', 'terms.html']) {
      await page.goto(base + file);
      for (const href of ['privacy.html', 'terms.html']) {
        const policyLinks = page.locator(`a[href="${href}"]`);
        for (const link of await policyLinks.all()) assert.equal(await link.getAttribute('target'), '_blank');
      }
      assert.equal(await page.locator('a[target="_blank"]:not([href="privacy.html"]):not([href="terms.html"])').count(), 0);
      const hrefs = await page.locator('a[href]').evaluateAll(anchors => anchors.map(a => a.getAttribute('href')));
      for (const href of hrefs) {
        if (/^(https?:|mailto:)/.test(href)) continue;
        assert(!href.startsWith('/'), `Root-relative path: ${href}`);
        const [name, fragment] = href.split('#');
        const local = path.join(root, name || file);
        assert(fs.existsSync(local), `Missing ${href} from ${file}`);
        if (fragment && local.endsWith('.html')) {
          const content = fs.readFileSync(local, 'utf8');
          assert(content.includes(`id="${fragment}"`), `Missing anchor ${href} from ${file}`);
        }
      }
    }
    const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
    const fallback = await noJS.newPage();
    await fallback.goto(base);
    assert.equal(await fallback.locator('#nav-links').isVisible(), true);
    for (const panel of ['mool', 'live', 'layout', 'workspace']) {
      assert.equal(await fallback.locator(`#panel-${panel}`).isVisible(), true);
    }
    results.push({ noJavaScript: 'Navigation, all product sections and native FAQ remain available' });
    await noJS.close();

    const imageErrorContext = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const errorPage = await imageErrorContext.newPage();
    await errorPage.route('**/images/product/live-3d-bench.webp', route => route.abort());
    await errorPage.goto(base);
    await errorPage.locator('.hero-screen .image-error').waitFor();
    results.push({ imageFailure: 'Accessible fallback message and direct image link displayed' });
    await imageErrorContext.close();

    await page.setViewportSize({ width: 1200, height: 630 });
    await page.goto(base);
    await page.evaluate(() => document.fonts.ready);
    await page.locator('.hero-screen img').evaluate(i => i.decode());
    await page.screenshot({ path: path.join(root, 'images', 'social-preview.png') });
    assert.equal(errors.length, 0, errors.join('\n'));
    assert.equal(failures.length, 0, failures.join('\n'));
    const report = { checkedAt: new Date().toISOString(), results, errors, failures };
    fs.writeFileSync(path.join(root, 'qa', 'verification.json'), JSON.stringify(report, null, 2));
    console.log(JSON.stringify({ status: 'passed', pagesAndViewports: 15, interactionChecks: 12, errors, failures }));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
