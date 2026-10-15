// Render only these locally generated diagrams using the host's existing runtime.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.RENDER_CHROMIUM,headless:true});
 const report={renderedAt:new Date().toISOString(),scope:'Offline local artifact rendering; all network requests blocked',figures:[]};
 const names=fs.readdirSync(__dirname).filter(n=>/^0[1-4].*\.html$/.test(n)).sort();
 for(const name of [...names,'index.html']){
  const page=await browser.newPage({viewport:{width:1360,height:900},deviceScaleFactor:2});
  await page.route('**/*',route=>route.request().url().startsWith('file:')?route.continue():route.abort());
  await page.goto(pathToFileURL(path.join(__dirname,name)).href);
  await page.evaluate(()=>document.fonts.ready);
  const geometry=await page.locator('svg').evaluateAll(svgs=>svgs.map(svg=>{
   const texts=[...svg.querySelectorAll('text')].map(t=>{const b=t.getBBox();return {text:t.textContent,x:b.x,y:b.y,w:b.width,h:b.height,font:getComputedStyle(t).fontFamily};});
   const out=texts.filter(b=>b.x<0||b.y<0||b.x+b.w>1280||b.y+b.h>720);
   const collisions=[];
   for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){
    let a=texts[i],b=texts[j];
    if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2)collisions.push([a.text,b.text]);
   }
   const diagonalLines=[...svg.querySelectorAll('line[marker-end]')].filter(l=>l.getAttribute('x1')!==l.getAttribute('x2')&&l.getAttribute('y1')!==l.getAttribute('y2')).length;
   return {outOfBounds:out,textCollisions:collisions,diagonalLines,nodes:svg.querySelectorAll('[data-node]').length,computedFont:texts[0]?.font};
  }));
  const cdp=await page.context().newCDPSession(page);await cdp.send('DOM.enable');await cdp.send('CSS.enable');
  const {root}=await cdp.send('DOM.getDocument');const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector:'svg text'});
  const fonts=await cdp.send('CSS.getPlatformFontsForNode',{nodeId});
  await page.setViewportSize({width:390,height:844});
  const mobile=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,localScrollers:[...document.querySelectorAll('.diagram-container')].map(e=>({client:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflowX}))}));
  await page.setViewportSize({width:1360,height:900});
  if(name!=='index.html'){
   const svg=page.locator('svg').first();
   await svg.evaluate(el=>{Object.assign(el.style,{width:'1280px',height:'720px',position:'absolute',left:'0',top:'0'});for(let a=el.parentElement;a;a=a.parentElement)a.style.setProperty('overflow','visible','important');});
   await svg.screenshot({path:path.join(__dirname,name.replace('.html','.png')),omitBackground:true});
  }
  report.figures.push({file:name,geometry,platformFonts:fonts.fonts,mobile});
  await page.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(__dirname,'render-verification.json'),JSON.stringify(report,null,2)+'\n');
 const problems=report.figures.filter(f=>f.geometry.some(g=>g.outOfBounds.length||g.textCollisions.length||g.diagonalLines)||f.mobile.documentWidth>f.mobile.width);
 console.log(JSON.stringify({files:report.figures.length,problems:problems.map(f=>({file:f.file,geometry:f.geometry,mobile:f.mobile})),fonts:report.figures[0].platformFonts},null,2));
 if(problems.length)process.exitCode=1;
})();
