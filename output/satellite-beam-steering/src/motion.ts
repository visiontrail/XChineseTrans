export const FPS=60;
export const DURATION=36;
export const FRAMES=FPS*DURATION;
export const clamp=(v:number)=>Math.max(0,Math.min(1,v));
export const smooth=(v:number)=>{const x=clamp(v);return x*x*x*(x*(x*6-15)+10)};
export const ramp=(t:number,a:number,b:number)=>smooth((t-a)/(b-a));
export const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
export const thetaAt=(t:number)=>30*ramp(t,1,4);
export const phaseStep=(theta:number)=>-180*Math.sin(theta*Math.PI/180);
export const arrayFactor=(theta:number,scan:number,n=8)=>{
 const psi=Math.PI*(Math.sin(theta*Math.PI/180)-Math.sin(scan*Math.PI/180));
 let re=0,im=0;for(let k=0;k<n;k++){re+=Math.cos(k*psi);im+=Math.sin(k*psi)}
 return Math.hypot(re,im)/n;
};
export const shotAt=(frame:number)=>Math.min(5,Math.floor(frame/360));
export const EVENTS=[0,6,12,18,24,30];
export const pointingState=(t:number)=>{
 const x=lerp(-2.45,2.45,ramp(t,0,6));
 const from=[x,2.4,0],target=[0,-2.3,0];
 return {x,y:2.9,from,target,theta:Math.atan2(-x,4.7)*180/Math.PI};
};
