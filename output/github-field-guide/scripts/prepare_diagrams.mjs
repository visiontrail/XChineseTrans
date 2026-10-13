import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from '/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.mjs';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const figures = [
  {name:'local-remote', out:'02-local-remote', title:'Where your work lives',
   subtitle:'Each command moves work to a different state.', height:375},
  {name:'pr-delivery', out:'06-pr-delivery', title:'A change needs evidence at every handoff',
   subtitle:'An example path from local edits to a usable static website.', height:430},
];
for (const figure of figures) {
  const filename = path.join(root,'diagrams',figure.name+'.html');
  let html = await fs.readFile(filename,'utf8');
  let svg = html.match(/<svg viewBox=[\s\S]*?<\/svg>/)[0];
  if (!svg.includes('editorial-refinement')) {
    svg = svg.replace(/<!-- Legend -->[\s\S]*?<\/svg>/, '</svg>');
    if (figure.name === 'local-remote') {
      svg = svg.replace('0 0 1040 430','0 0 1040 375');
      svg = svg.replaceAll('font-size="11"','font-size="14"').replaceAll('font-size="9"','font-size="11"').replaceAll('font-size="8"','font-size="11"');
      const labels = svg.indexOf('<!-- Connection labels -->');
      svg = svg.slice(0,labels) + svg.slice(labels).replace(/<rect [^>]+class="c-mask"\/>/g,'');
      svg = svg.replace('</svg>', `<!-- editorial-refinement -->
        <rect x="70" y="270" width="310" height="70" rx="6" class="c-external"/>
        <text x="86" y="292" class="t-primary" font-size="13" font-weight="600">Stage the content you intend.</text>
        <text x="86" y="314" class="t-muted" font-size="11">Later edits need another git add.</text>
        <rect x="410" y="270" width="335" height="70" rx="6" class="c-external"/>
        <text x="426" y="292" class="t-primary" font-size="13" font-weight="600">Fetch is a download, not a merge.</text>
        <text x="426" y="314" class="t-muted" font-size="11">Inspect remote history before integrating.</text>
        </svg>`);
    } else {
      svg = svg.replace('0 0 720 528','0 0 720 430');
      svg = svg.replaceAll('font-size="11"','font-size="13"').replaceAll('font-size="8"','font-size="9"');
      svg = svg.replace('01 / 01 / LOCAL WORK','01 / LOCAL WORK').replace('02 / 02 / GITHUB REVIEW','02 / GITHUB REVIEW').replace('03 / 03 / DELIVERY','03 / DELIVERY');
      svg = svg.replaceAll('class="t-dim" font-size="10"','class="t-muted" font-size="10"');
      svg = svg.replace('</svg>','<!-- editorial-refinement --></svg>');
    }
    html = html.replace(/<svg viewBox=[\s\S]*?<\/svg>/,svg);
    await fs.writeFile(filename,html);
  }
  const lightBlock = html.match(/\[data-theme="light"\]\s*\{([\s\S]*?)\}/)[1];
  const vars = Object.fromEntries([...lightBlock.matchAll(/(--[\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
  let css = html.slice(html.indexOf('    .c-grid'),html.indexOf('</style>',html.indexOf('    .c-grid')));
  css = css.replace(/var\((--[\w-]+)\)/g,(_,key)=>vars[key]);
  css += '\ntext{font-family:Arial,Helvetica,sans-serif}';
  const [,, w,h] = svg.match(/viewBox="([\d]+) ([\d]+) ([\d]+) ([\d]+)"/).slice(1).map(Number);
  const content = svg.replace(/^<svg[^>]*>/,'').replace(/<\/svg>$/,'');
  const exported = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h+105}" viewBox="0 0 ${w} ${h+105}">
    <style>${css}</style>
    <rect width="100%" height="100%" fill="#f8fafc"/>
    <text x="40" y="38" fill="#102839" font-family="Arial,sans-serif" font-size="${w>900?27:23}" font-weight="700">${figure.title}</text>
    <text x="40" y="63" fill="#526574" font-family="Arial,sans-serif" font-size="14">${figure.subtitle}</text>
    <g transform="translate(0,75)">${content}</g>
    <text x="40" y="${h+92}" fill="#526574" font-family="Arial,sans-serif" font-size="10">LEOGUOLABS  /  GITHUB FIELD GUIDE  /  CONCEPTUAL DIAGRAM</text>
  </svg>`;
  await fs.writeFile(path.join(root,'diagrams',figure.name+'.svg'),exported);
  await sharp(Buffer.from(exported)).resize({width:2200}).png().toFile(path.join(root,'images',figure.out+'.png'));
  console.log(figure.out+'.png');
}
