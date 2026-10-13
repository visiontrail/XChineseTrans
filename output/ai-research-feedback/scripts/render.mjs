import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(),T=JSON.parse(fs.readFileSync('public/timeline.json'));
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),publicDir:path.join(root,'public'),outDir:path.join(root,'.bundle')});
const composition=await selectComposition({serveUrl,id:'AIResearchFeedback'});
const t0=Date.now();
if(process.argv.includes('--stills')){
 const frames=T.shots.map(s=>Math.min(s.end-20,s.start+Math.round((s.end-s.start)*.68)));
 for(const frame of frames){await renderStill({serveUrl,composition,frame,output:path.join(root,`frames/frame-${String(frame).padStart(5,'0')}.png`),imageFormat:'png'});console.log(`still ${frame}`);}
 fs.writeFileSync('evidence/stills-render.json',JSON.stringify({frames,seconds:(Date.now()-t0)/1000},null,2));
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,codec:'h264',crf:19,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'192k',outputLocation:path.join(root,'research-feedback-v1.mp4'),concurrency:4,onProgress:({progress})=>{const p=Math.floor(progress*100);if(p>=last+5){console.log(`render ${p}%`);last=p;}}});
 fs.writeFileSync('evidence/render.json',JSON.stringify({composition,seconds:(Date.now()-t0)/1000,finishedAt:new Date().toISOString(),codec:'h264',crf:19,concurrency:4},null,2));console.log('render complete');
}
