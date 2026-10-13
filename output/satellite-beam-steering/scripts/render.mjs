import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import fs from 'node:fs';import path from 'node:path';
const root=process.cwd();
const legacy=path.resolve('../codex-motion-routing/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell');
const browserExecutable=fs.existsSync(legacy)?legacy:undefined;
const chromiumOptions={gl:'angle'};
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),publicDir:path.join(root,'public'),outDir:path.join(root,'.bundle')});
const composition=await selectComposition({serveUrl,id:'SteeringWithoutTurning',browserExecutable,chromiumOptions});
const t0=Date.now();
if(process.argv.includes('--stills')){
 const option=process.argv.find(a=>a.startsWith('--frames='));
 const frames=option?option.split('=')[1].split(',').map(Number):[150,510,870,1110,1320,1590,1950,2159];
 for(const frame of frames){await renderStill({serveUrl,composition,frame,output:path.join(root,`frames/frame-${String(frame).padStart(4,'0')}.png`),imageFormat:'png',browserExecutable,chromiumOptions});console.log(`still ${frame}`);}
 fs.writeFileSync('evidence/stills-render.json',JSON.stringify({frames,seconds:(Date.now()-t0)/1000},null,2));
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,codec:'h264',crf:17,pixelFormat:'yuv420p',audioCodec:'aac',audioBitrate:'256k',outputLocation:path.join(root,'steering-without-turning-v1.mp4'),concurrency:3,browserExecutable,chromiumOptions,onProgress:({progress})=>{const p=Math.floor(progress*100);if(p>=last+5){console.log(`render ${p}%`);last=p;}}});
 fs.writeFileSync('evidence/render.json',JSON.stringify({composition,seconds:(Date.now()-t0)/1000,finishedAt:new Date().toISOString(),codec:'h264',crf:17,concurrency:3,renderer:'Three.js WebGL / ANGLE'},null,2));console.log('render complete');
}
