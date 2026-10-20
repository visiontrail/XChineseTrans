const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core');

(async () => {
  const dir = __dirname;
  const slug = 'actions-lockfiles-flow-v1';
  const browser = await chromium.launch({executablePath:'/Users/leoguo/Library/Caches/ms-playwright/chromium-1161/chrome-mac/Chromium.app/Contents/MacOS/Chromium',headless:true});
  const page = await browser.newPage({viewport:{width:1080,height:1080},deviceScaleFactor:2});
  const errors = [];
  const requests = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('request', r => requests.push(r.url()));
  await page.goto(pathToFileURL(path.join(dir,slug+'.html')).href, {waitUntil:'load'});
  await page.evaluate(() => document.fonts.ready);
  const qa = await page.evaluate(() => {
    const svg = document.querySelector('svg');
    const bounds = e => {const b=e.getBBox(); return {x:b.x,y:b.y,w:b.width,h:b.height};};
    const texts = [...svg.querySelectorAll('text')].map(e => ({text:e.textContent,...bounds(e),font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize}));
    const outOfCanvas = texts.filter(b => b.x<56||b.y<56||b.x+b.w>1024||b.y+b.h>1052);
    const overlaps = [];
    for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){
      const a=texts[i],b=texts[j];
      if(a.x < b.x+b.w && a.x+a.w>b.x && a.y<b.y+b.h && a.y+a.h>b.y) overlaps.push([a.text,b.text]);
    }
    const nodeFit = [...svg.querySelectorAll('[data-node]')].map(n=>{
      const r=n.querySelector('rect').getBBox();
      return {node:n.dataset.node,overflow:[...n.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<r.x+16||b.x+b.width>r.x+r.width-16||b.y<r.y+10||b.y+b.height>r.y+r.height-10;}).map(t=>t.textContent)};
    });
    return {viewBox:svg.getAttribute('viewBox'),nodeCount:document.querySelectorAll('[data-node]').length,edgeCount:document.querySelectorAll('[data-edge]').length,fontReady:document.fonts.check('600 36px Geist'),fontFaces:[...document.fonts].map(f=>({family:f.family,weight:f.weight,status:f.status})),outOfCanvas,overlaps,nodeFit,texts};
  });
  await page.locator('svg').screenshot({path:path.join(dir,slug+'.png'),omitBackground:true});
  await page.setViewportSize({width:390,height:844});
  const mobile = await page.evaluate(()=>({pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,scrollerWidth:document.querySelector('.diagram-container').clientWidth,scrollerContentWidth:document.querySelector('.diagram-container').scrollWidth}));
  await page.screenshot({path:path.join(dir,'qa-html-mobile.png')});
  // Separate practical thumbnail: the complete export at a 390px feed width.
  await page.setContent(`<html><body style="margin:0"><img src="${pathToFileURL(path.join(dir,slug+'.png')).href}" style="display:block;width:390px;height:390px"></body></html>`);
  await page.locator('img').waitFor();
  await page.locator('img').screenshot({path:path.join(dir,'qa-feed-390.png')});
  qa.mobile = mobile;
  qa.pageErrors = errors;
  qa.externalRequests = requests.filter(u=>/^https?:/.test(u));
  fs.writeFileSync(path.join(dir,'qa.json'), JSON.stringify(qa,null,2)+'\n');
  console.log(JSON.stringify({...qa,texts:undefined},null,2));
  await browser.close();
  if (qa.outOfCanvas.length || qa.overlaps.length || qa.nodeFit.some(n=>n.overflow.length) || errors.length || !qa.fontReady || qa.fontFaces.some(f=>f.status!=='loaded')) process.exit(1);
})();
