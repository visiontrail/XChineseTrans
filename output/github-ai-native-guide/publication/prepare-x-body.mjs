import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {marked} from '/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here);
const md=await fs.readFile(path.join(root,'article.md'),'utf8');
let body=marked.parse(md).replace(/^<h1>[\s\S]*?<\/h1>\s*/,'');
// X Articles accepts block quotes, headings and lists. Preserve prompt text,
// while adapting its display from the local reader's custom prompt cards.
body=body.replace(/<pre><code class="language-prompt">([\s\S]*?)<\/code><\/pre>/g,
  (_,s)=>'<blockquote><p>'+s.trimEnd().replaceAll('\n','<br>')+'</p></blockquote>');
// Preserve every table cell as a readable labeled list in X's native editor.
body=body.replace(/<table>([\s\S]*?)<\/table>/g,(_,table)=>{
  const headers=[...table.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map(m=>m[1]);
  const rows=[...table.matchAll(/<tr>([\s\S]*?)<\/tr>/g)]
    .map(m=>[...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map(c=>c[1])).filter(x=>x.length);
  return '<p><strong>'+headers.join(' · ')+'</strong></p><ul>'+rows.map(row=>
    '<li><strong>'+row[0]+'</strong><br>'+row.slice(1).map((cell,i)=>headers[i+1]+': '+cell).join('<br>')+'</li>').join('')+'</ul>';
});
const matches=[...body.matchAll(/<p><img src="([^"]+)" alt="([^"]*)"><\/p>/g)];
if(matches.length!==12)throw Error('Expected 12 images');
const parts=[]; let cursor=0;
for(let i=0;i<matches.length;i++){
  const m=matches[i];
  if(i===0){body=body.slice(0,m.index)+body.slice(m.index+m[0].length);break;}
}
cursor=0;
for(const m of body.matchAll(/<p><img src="([^"]+)" alt="([^"]*)"><\/p>/g)){
  parts.push({html:body.slice(cursor,m.index).trim(),imageAfter:m[1],alt:m[2]});
  cursor=m.index+m[0].length;
}
parts.push({html:body.slice(cursor).trim(),imageAfter:null});
await fs.writeFile(path.join(here,'x-body-parts.json'),JSON.stringify(parts,null,2)+'\n');
await fs.writeFile(path.join(here,'x-body.html'),body);
console.log(JSON.stringify({parts:parts.length,inlineFigures:parts.filter(p=>p.imageAfter).length,promptQuotes:(body.match(/<blockquote>/g)||[]).length}));
