import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {marked} from '/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';

const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const md=await fs.readFile(path.join(root,'article.md'),'utf8');
const esc=s=>s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const strip=s=>s.replace(/<[^>]*>/g,'');
let content=marked.parse(md,{gfm:true});
const title=strip(content.match(/<h1>(.*?)<\/h1>/s)[1]);
content=content.replace(/<h1>.*?<\/h1>\s*/s,'');
const deck=strip(content.match(/^<p>(.*?)<\/p>/s)[1]);
content=content.replace(/^<p>.*?<\/p>\s*/s,'');
let i=0;
const assets=[];
content=content.replace(/<p><img src="([^"]+)" alt="([^"]*)"><\/p>\s*<p><em>([\s\S]*?)<\/em><\/p>/g,(_,src,alt,caption)=>{
  i++; assets.push({number:i,file:src,alt,caption:strip(caption)});
  return `<figure id="figure-${i}" class="figure ${i===1?'cover':''}"><button type="button" class="figure-open" aria-label="Enlarge figure ${i}: ${alt}"><img src="${src}" alt="${alt}" decoding="async"></button><figcaption><span class="figure-number">FIG. ${String(i).padStart(2,'0')}</span><span>${caption}</span></figcaption></figure>`;
});
if(i!==7) throw Error(`Expected 7 figures, found ${i}`);
content=content.replace('href="screenshots/originals/01-repository.png"','class="original-capture" href="screenshots/originals/01-repository.png"');
const hero=content.match(/^<figure[\s\S]*?<\/figure>/)[0];
content=content.slice(hero.length);
const toc=[];
content=content.replace(/<h2>(.*?)<\/h2>/g,(_,heading)=>{
  const [number,...rest]=heading.split('. '); const text=rest.join('. ');
  const id='section-'+number; toc.push({number,text,id});
  return `<h2 id="${id}"><span class="section-no">${String(number).padStart(2,'0')}</span>${text}</h2>`;
});
content=content.replace(/<table>[\s\S]*?<\/table>/g,table=>`<div class="table-scroll" role="region" aria-label="Reference table" tabindex="0">${table}</div>`);
let html=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="${esc(deck)}"><meta name="color-scheme" content="light"><title>${esc(title)} · LeoGuoLabs</title>
<style>
:root{--paper:#f7f4ed;--ink:#173042;--muted:#54616a;--line:#d7d8cc;--teal:#006b68;--orange:#b95425;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;--serif:Georgia,'Palatino Linotype',serif}
*{box-sizing:border-box}html{scroll-behavior:auto;scroll-padding-top:30px}body{margin:0;background:var(--paper);color:var(--ink);font:19px/1.75 var(--serif)}a{color:var(--teal);text-underline-offset:.2em;text-decoration-thickness:1px}a:hover{text-decoration-thickness:2px}button{font:inherit}button:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--orange);outline-offset:5px}.shell{max-width:1240px;margin:auto;padding:0 40px}.masthead{display:flex;justify-content:space-between;gap:24px;padding:26px 0 20px;border-bottom:1px solid var(--ink);font:11px/1.5 var(--mono);letter-spacing:.16em}.brand{font-weight:700;letter-spacing:.18em}.edition{color:var(--muted)}.hero{padding-top:42px}.eyebrow{font:11px/1.5 var(--mono);letter-spacing:.18em;color:var(--orange);margin:0 0 15px}.hero h1{max-width:1050px;font:normal clamp(44px,5.4vw,76px)/1.08 var(--serif);letter-spacing:-.045em;margin:0 0 20px}.deck{max-width:820px;font:21px/1.55 var(--sans);color:var(--muted);margin:0}.byline{margin:22px 0 30px;display:flex;gap:24px;flex-wrap:wrap;font:11px/1.6 var(--mono);letter-spacing:.06em}.byline strong{font-weight:600}.figure{margin:34px 0 38px}.figure img{display:block;width:100%;height:auto}.figure-open{display:block;width:100%;padding:0;background:transparent;border:1px solid var(--line);cursor:zoom-in;overflow:hidden}.cover{margin-top:0}.cover .figure-open{border:0}figcaption{display:flex;gap:18px;margin-top:11px;font:12px/1.6 var(--sans);color:var(--muted)}.figure-number{flex-shrink:0;font:10px/1.8 var(--mono);letter-spacing:.08em;color:var(--orange)}.reading-grid{display:grid;grid-template-columns:208px minmax(0,1fr);gap:56px;align-items:start;margin-top:52px}.toc{position:sticky;top:28px;border-top:2px solid var(--teal);padding-top:15px;font-family:var(--sans)}.toc summary{font:11px/1.5 var(--mono);letter-spacing:.13em;cursor:pointer}.toc ol{list-style:none;padding:0;margin:17px 0}.toc li{margin:0 0 11px}.toc a{display:grid;grid-template-columns:22px 1fr;gap:7px;text-decoration:none;color:var(--muted);font:12px/1.4 var(--sans)}.toc a:hover{color:var(--teal)}.toc .num{font:10px/1.7 var(--mono);color:var(--orange)}.article{min-width:0}.article>p:first-child{font-size:24px;line-height:1.6}.article p{margin:0 0 22px}.article h2{border-top:1px solid var(--line);padding-top:34px;margin:65px 0 24px;font:normal 35px/1.2 var(--serif);letter-spacing:-.025em;scroll-margin-top:28px}.section-no{display:block;color:var(--orange);font:12px/1.6 var(--mono);letter-spacing:.12em;margin-bottom:10px}.article h3{font:600 20px/1.4 var(--sans);margin:38px 0 18px}.article li{padding-left:3px;margin:10px 0}.article ul,.article ol{padding-left:26px}.article strong{font-weight:700}.article em{font-style:italic}.article code{font: .8em/1.6 var(--mono);background:#e9ede5;border-radius:3px;padding:2px 5px;overflow-wrap:anywhere}.article pre{margin:24px 0 28px;padding:23px 25px;background:#142c3d;color:#e9eeea;overflow-x:auto;border-left:3px solid #35a79b;border-radius:0 4px 4px 0;font:13px/1.7 var(--mono);tab-size:2}.article pre code{padding:0;background:none;font:inherit;overflow-wrap:normal}.table-scroll{max-width:100%;overflow-x:auto;margin:25px 0 30px;border-top:2px solid var(--ink);border-bottom:1px solid var(--line)}table{border-collapse:collapse;width:100%;font:14px/1.6 var(--sans)}th,td{text-align:left;vertical-align:top;padding:13px 13px;border-bottom:1px solid var(--line)}th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);background:#eeeede}tr:last-child td{border-bottom:0}td:first-child{font-weight:600;min-width:125px}table code{font-size:12px}.footer{margin:70px 0 34px;padding-top:22px;border-top:1px solid var(--ink);display:flex;justify-content:space-between;gap:28px;font:11px/1.6 var(--mono);color:var(--muted)}.footer a{white-space:nowrap}.lightbox{padding:22px;max-width:96vw;max-height:96vh;border:0;background:#f7f4ed;color:var(--ink)}.lightbox::backdrop{background:#0d2133dc;backdrop-filter:blur(4px)}.lightbox img{display:block;max-width:calc(96vw - 44px);max-height:78vh;object-fit:contain;margin:auto}.lightbox p{font:13px/1.5 var(--sans);max-width:90vw;margin:14px 0 0}.lightbox-close{display:block;margin:0 0 15px auto;background:var(--ink);border:0;color:white;padding:7px 14px;font:12px/1.5 var(--sans);cursor:pointer}.skip{position:absolute;left:20px;top:-100px;background:var(--paper);padding:12px;z-index:20}.skip:focus{top:12px}
@media(max-width:900px){.shell{padding:0 24px}.reading-grid{grid-template-columns:1fr;gap:26px;margin-top:36px}.toc{position:static;padding:13px 0;border-bottom:1px solid var(--line)}.toc ol{columns:2;column-gap:24px}.toc li{break-inside:avoid}.article h2{margin-top:50px}.hero h1{max-width:800px}.hero{padding-top:30px}}
@media(max-width:520px){body{font-size:17px;line-height:1.75}.shell{padding:0 19px}.masthead{padding:19px 0 15px;font-size:9px;gap:15px;letter-spacing:.08em}.brand{white-space:nowrap}.edition{text-align:right}.hero h1{font-size:43px;letter-spacing:-.04em}.eyebrow{font-size:9px}.deck{font-size:18px;line-height:1.5}.byline{gap:8px 18px;font-size:9px;margin:17px 0 25px}.figure{margin:26px 0}figcaption{font-size:11px;gap:11px}.figure-number{font-size:9px}.toc ol{columns:1}.toc a{font-size:13px}.article>p:first-child{font-size:21px}.article h2{font-size:29px;line-height:1.25;padding-top:25px}.article h3{font-size:19px}.article pre{padding:17px 18px;font-size:11.5px;margin-left:-3px;margin-right:-3px}.table-scroll table{min-width:560px}th,td{padding:11px}.footer{display:block;font-size:10px}.footer a{display:block;margin-top:10px}.lightbox{padding:12px}.lightbox img{max-width:calc(96vw - 24px)}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{body{background:white;font-size:11pt}.shell{max-width:none;padding:0}.masthead,.byline{font-size:8pt}.hero h1{font-size:34pt}.deck{font-size:13pt}.toc,.footer,.lightbox{display:none}.reading-grid{display:block}.article h2{font-size:20pt;break-after:avoid}.article h3{font-size:13pt;break-after:avoid}.article p,.article li{orphans:3;widows:3}.article pre{color:#142c3d;background:#eef0ee;white-space:pre-wrap;font-size:8pt;break-inside:avoid}.table-scroll{overflow:visible}.figure{break-inside:avoid}figcaption{font-size:8pt}.figure-open{border:0}.cover{max-width:85%;margin:auto}a{color:inherit}table{font-size:9pt}}
</style></head><body id="top"><a class="skip" href="#article">Skip to article</a><div class="shell">
<header class="masthead"><span class="brand">LEOGUOLABS</span><span class="edition">ENGINEERING FIELD NOTES · 27 SEP 2026</span></header>
<section class="hero" aria-labelledby="article-title"><p class="eyebrow">A PRACTICAL GUIDE / GIT & GITHUB</p><h1 id="article-title">${esc(title)}</h1><p class="deck">${esc(deck)}</p><p class="byline"><strong>BY LEOGUOLABS</strong><span>15 SECTIONS</span><span>7 ORIGINAL FIGURES & FRESH CAPTURES</span></p>${hero}</section>
<div class="reading-grid"><aside class="toc"><details open id="toc"><summary>IN THIS GUIDE</summary><nav aria-label="Table of contents"><ol>${toc.map(t=>`<li><a href="#${t.id}"><span class="num">${String(t.number).padStart(2,'0')}</span><span>${t.text}</span></a></li>`).join('')}</ol></nav></details></aside><main id="article" class="article">${content}</main></div>
<footer class="footer"><span>LEOGUOLABS · ENGINEERING FIELD NOTES<br>Read the change. Check the result.</span><a href="#top">Back to the beginning ↑</a></footer></div>
<dialog class="lightbox" aria-label="Enlarged figure"><button class="lightbox-close" type="button">Close · Esc</button><img alt=""><p></p></dialog>
<script>
const dialog=document.querySelector('.lightbox');
document.querySelectorAll('.figure-open').forEach(button=>button.addEventListener('click',()=>{const source=button.querySelector('img');dialog.querySelector('img').src=source.src;dialog.querySelector('img').alt=source.alt;dialog.querySelector('p').textContent=button.closest('figure').querySelector('figcaption').innerText;dialog.showModal();}));
document.querySelector('.original-capture').addEventListener('click',event=>{event.preventDefault();dialog.querySelector('img').src=event.currentTarget.href;dialog.querySelector('img').alt='Unedited local capture of the Flask repository';dialog.querySelector('p').textContent='Unedited capture, taken on this computer on 27 September 2026.';dialog.showModal();});
document.querySelector('.lightbox-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
if(matchMedia('(max-width:900px)').matches)document.querySelector('#toc').open=false;
</script></body></html>`;
// Embed every figure and the unedited reference capture; the long read works offline.
const localAssets=[...new Set([...html.matchAll(/(?:src|href)="((?:images|screenshots)\/[^\"]+)"/g)].map(m=>m[1]))];
for(const local of localAssets){const bytes=await fs.readFile(path.join(root,local));html=html.replaceAll('"'+local+'"','"data:image/png;base64,'+bytes.toString('base64')+'"');}
await fs.writeFile(path.join(root,'article.html'),html);
await fs.writeFile(path.join(root,'research/rendered-body.html'),marked.parse(md));
await fs.writeFile(path.join(root,'alt-text.md'),'# Figure order and ALT text\n\n'+assets.map(a=>`## ${a.number}. ${a.file}\n\n${a.alt}\n\nCaption: ${a.caption}\n`).join('\n'));
console.log(JSON.stringify({figures:assets.length,sections:toc.length,embeddedAssets:localAssets.length,htmlBytes:Buffer.byteLength(html)}));
