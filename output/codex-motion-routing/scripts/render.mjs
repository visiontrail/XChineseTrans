import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd();
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),publicDir:path.join(root,'public'),outDir:path.join(root,'.bundle')});
const composition=await selectComposition({serveUrl,id:'RouteAroundFailure'});
const t0=Date.now();
if(process.argv.includes('--stills')){
 const frames=[90,330,420,478,480,485,500,540,720,810,870,960,990,1110,1122,1260,1350,1439];
 for(const frame of frames){await renderStill({serveUrl,composition,frame,output:path.join(root,`frames/frame-${String(frame).padStart(4,'0')}.png`),imageFormat:'png'});console.log(`still ${frame}`);}
 fs.writeFileSync('evidence/stills-render.json',JSON.stringify({frames,seconds:(Date.now()-t0)/1000},null,2));
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,codec:'h264',crf:18,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'256k',outputLocation:path.join(root,'route-around-failure-v1.mp4'),concurrency:4,onProgress:({progress})=>{const p=Math.floor(progress*100);if(p>=last+10){console.log(`render ${p}%`);last=p;}}});
 fs.writeFileSync('evidence/render.json',JSON.stringify({composition,seconds:(Date.now()-t0)/1000,finishedAt:new Date().toISOString(),codec:'h264',crf:18,concurrency:4},null,2));
 console.log('render complete');
}
