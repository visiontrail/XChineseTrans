import fs from 'node:fs';
import {buildSync} from 'esbuild';
buildSync({entryPoints:['src/motion.ts'],bundle:true,platform:'node',format:'esm',outfile:'.motion-check.mjs'});
const {heroMetrics,T}=await import('../.motion-check.mjs');
let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity,maxStep=0,maxAspect=0;
const problems=[];
for(let f=0;f<T.durationFrames;f++){
 const h=heroMetrics(f),prev=heroMetrics(Math.max(0,f-1));
 minX=Math.min(minX,h.x-h.radius*h.sx);maxX=Math.max(maxX,h.x+h.radius*h.sx);
 minY=Math.min(minY,h.y-h.radius*h.sx);maxY=Math.max(maxY,h.y+h.radius*h.sx);
 maxStep=Math.max(maxStep,Math.hypot(h.x-prev.x,h.y-prev.y));maxAspect=Math.max(maxAspect,h.sx/h.sy);
 if(!Object.values(h).every(Number.isFinite))problems.push({frame:f,reason:'nonfinite'});
}
if(minX<100||maxX>1820||minY<100||maxY>960)problems.push({reason:'subject safe-area violation'});
if(maxStep>40)problems.push({reason:'subject position discontinuity',maxStep});
const report={frames:T.durationFrames,events:T.events.length,minX,maxX,minY,maxY,maxStep,maxAspect,problems,passed:problems.length===0};
fs.writeFileSync('evidence/motion-check.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
if(problems.length)process.exitCode=1;
