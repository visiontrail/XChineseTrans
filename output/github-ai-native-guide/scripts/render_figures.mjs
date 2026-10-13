import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import sharp from '/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.mjs';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
for(const name of (await fs.readdir(path.join(root,'diagrams'))).filter(x=>x.endsWith('.architecture.json')).sort()){
  const id=name.replace('.architecture.json','');
  const spec=JSON.parse(await fs.readFile(path.join(root,'diagrams',name),'utf8'));
  const extra=JSON.parse(await fs.readFile(path.join(root,'diagrams',id+'.notes.json'),'utf8'));
  const filename=path.join(root,'diagrams',id+'.html');
  let html=await fs.readFile(filename,'utf8');
  let svg=html.match(/<svg viewBox=[\s\S]*?<\/svg>/)[0];
  const [w,h]=spec.meta.viewBox;
  svg=svg.replace(/<!-- Legend -->[\s\S]*?<\/svg>/,'</svg>');
  svg=svg.replaceAll('font-size="11"','font-size="14"').replaceAll('font-size="9"','font-size="11"').replaceAll('font-size="8"','font-size="11"');
  // Keep labels above their routes and give them a mask sized for the final font.
  svg=svg.replace(/<rect x="[^"]+" y="([^"]+)" width="[^"]+" height="14" rx="3" class="c-mask"\/>\s*<text x="([^"]+)" y="([^"]+)" class="([^"]+)" font-size="11" text-anchor="middle">([^<]+)<\/text>/g,(_,ry,x,y,cls,label)=>{
    const width=label.length*6.7+14;
    return `<rect x="${Number(x)-width/2}" y="${Number(y)-12}" width="${width}" height="17" rx="3" class="c-mask"/><text x="${x}" y="${y}" class="${cls}" font-size="11" text-anchor="middle">${label}</text>`;
  });
  let notes='<!-- editorial-notes -->';
  extra.headings.forEach(([s,x,y])=>{notes+=`<text x="${x}" y="${y}" class="t-primary" font-size="14" font-weight="600">${esc(s)}</text>`;});
  extra.notes.forEach((s,i)=>{notes+=`<text x="50" y="${h-26-(extra.notes.length-1-i)*23}" class="t-muted" font-size="12">${esc(s)}</text>`;});
  svg=svg.replace('</svg>',notes+'</svg>');
  html=html.replace(/<svg viewBox=[\s\S]*?<\/svg>/,svg);
  await fs.writeFile(filename,html);
  const block=html.match(/\[data-theme="light"\]\s*\{([\s\S]*?)\}/)[1];
  const vars=Object.fromEntries([...block.matchAll(/(--[\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
  let css=html.slice(html.indexOf('    .c-grid'),html.indexOf('</style>',html.indexOf('    .c-grid')));
  css=css.replace(/var\((--[\w-]+)\)/g,(_,key)=>vars[key]);
  css+='\ntext{font-family:Menlo,Consolas,monospace}';
  const content=svg.replace(/^<svg[^>]*>/,'').replace(/<\/svg>$/,'');
  const exportSvg=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h+110}" viewBox="0 0 ${w} ${h+110}"><style>${css}</style><rect width="100%" height="100%" fill="#f8fafc"/><text x="50" y="37" fill="#163145" style="font-family:Georgia,serif" font-size="28" font-weight="700">${esc(spec.meta.title)}</text><text x="50" y="63" fill="#526574" style="font-family:Arial,sans-serif" font-size="14">${esc(spec.meta.subtitle)}</text><g transform="translate(0,78)">${content}</g><text x="50" y="${h+99}" fill="#526574" font-size="10">LEOGUOLABS / GIT, THE AI-NATIVE WAY / CONCEPTUAL DIAGRAM ${id.slice(0,2)}</text></svg>`;
  await fs.writeFile(path.join(root,'diagrams',id+'.svg'),exportSvg);
  await sharp(Buffer.from(exportSvg)).resize({width:2200}).png().toFile(path.join(root,'images',id+'.png'));
  console.log(id);
}
