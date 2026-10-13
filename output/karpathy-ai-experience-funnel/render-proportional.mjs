import fs from 'node:fs/promises';
import sharp from '/Users/leoguo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/dist/index.mjs';
const out = new URL('./', import.meta.url);
const W=1440, H=1800, center=460, topWidth=760, bottomWidth=760*2/3, h=176;
const counts=[6e9,1.5e9,20e6,5000];
const labels=[['~6B','Little or no','LLM exposure'],['~1–2B','Casual free-tier','users'],['~20M','Frontier tools for','math & code'],['~5,000','Internal frontier','systems']];
let elements=[], measurements=[];
const text=(x,y,s,size=36,fill='#1A4A3A',weight=400)=>`<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" font-weight="${weight}">${s.replaceAll("&","&amp;").replaceAll("<","&lt;")}</text>`;
for(let i=0;i<4;i++){
 const factor=counts[i]/counts[0], tw=topWidth*factor, bw=bottomWidth*factor,y=460+i*235;
 const points=`${center-tw/2},${y} ${center+tw/2},${y} ${center+bw/2},${y+h} ${center-bw/2},${y+h}`;
 elements.push(`<polygon points="${points}" fill="#DDE6DB" stroke="none"/>`);
 // Leader lines are annotation, not a minimum width or a dot for the data.
 elements.push(`<path d="M ${center+(tw+bw)/4+18} ${y+h/2} H 900" stroke="#B4C1B4" stroke-width="1.5" fill="none"/>`);
 elements.push(text(930,y+73,labels[i][0],82,'#80601B',600));
 elements.push(text(930,y+122,labels[i][1],35));
 elements.push(text(930,y+166,labels[i][2],35));
 measurements.push({count:counts[i],top_width:tw,bottom_width:bw,height:h,area:(tw+bw)*h/2,ratio_to_6B:factor});
}
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.72" numOctaves="3" stitchTiles="stitch"/></filter></defs>
<rect width="1440" height="1800" fill="#FDFBF7"/><rect width="1440" height="1800" filter="url(#grain)" opacity="0.025"/>
<g font-family="Helvetica Neue,Arial,sans-serif">
${text(86,157,'The AI',96,'#1A4A3A',600)}
${text(86,268,'experience gap',96,'#1A4A3A',600)}
${text(86,358,'Billions have barely encountered an LLM.',43)}
${elements.join('\n')}
${text(86,1449,'6B ÷ 5,000 = 1,200,000×',53,'#80601B',500)}
${text(86,1506,'The smallest group is below one pixel at this scale.',32,'#426454')}
<path d="M 86 1552 H 1354" stroke="#1A4A3A" stroke-width="1.5"/>
${text(86,1614,'Task size · Domain · Access',43,'#1A4A3A',500)}
${text(86,1680,'Segment areas scale linearly with Karpathy’s rough estimates.',27,'#426454')}
${text(86,1724,'1–2B shown at midpoint: 1.5B.',27,'#426454')}
${text(1135,1758,'LeoGuoLabs',30)}
</g></svg>`;
await fs.writeFile(new URL('funnel-proportional-v3.svg',out),svg);
await sharp(Buffer.from(svg)).png().toFile(new URL('funnel-proportional-v3.png',out).pathname);
const scale=measurements[0].area/counts[0];
for(let i=0;i<measurements.length;i++){if(Math.abs(measurements[i].area/counts[i]-scale)>scale*1e-12)throw new Error('Area ratio mismatch');}
await fs.writeFile(new URL('proportion-check.json',out),JSON.stringify({width:W,height:H,method:'Equal-height trapezoids with top and bottom widths scaled by count; no stroke or minimum pixel width',middle_count:'1.5B midpoint of stated 1–2B range',measurements,area_per_person:scale,all_area_ratios_verified:true},null,2));
