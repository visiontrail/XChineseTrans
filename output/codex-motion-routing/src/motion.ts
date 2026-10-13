import timeline from '../public/timeline.json';
export const T = timeline;
export const event = (id:string) => T.events.find(e=>e.id===id)!.frame;
export const clamp = (v:number,a=0,b=1)=>Math.min(b,Math.max(a,v));
export const ease = (v:number)=>{const t=clamp(v); return t*t*t*(t*(6*t-15)+10);};
export const prog = (f:number,a:number,b:number)=>ease((f-a)/(b-a));
export const mix = (a:number,b:number,p:number)=>a+(b-a)*p;
export type P = {x:number,y:number};
export const lerp = (a:P,b:P,p:number):P=>({x:mix(a.x,b.x,p),y:mix(a.y,b.y,p)});
export const bezier = (a:P,b:P,c:P,d:P,p:number):P=>{
 const q=1-p;return {x:q*q*q*a.x+3*q*q*p*b.x+3*q*p*p*c.x+p*p*p*d.x,y:q*q*q*a.y+3*q*q*p*b.y+3*q*p*p*c.y+p*p*p*d.y};
};
export const impulse = (f:number,start:number,amp=1,decay=0.10,frequency=0.20)=>{
 const t=f-start;return t<0?0:amp*Math.exp(-decay*t)*Math.sin(frequency*t);
};
export const N = {source:{x:320,y:620},router:{x:780,y:620},a:{x:1000,y:380},b:{x:1320,y:380},dest:{x:1610,y:620},lower:{x:1110,y:830}};
export function hero(f:number):P {
 const unfold=event('unfold'),launch=event('launch'),router=event('router'),depart=event('depart'),a=event('upper-a'),b=event('upper-b'),arrival=event('arrival'),close=event('close');
 const opening={x:1430,y:550+10*Math.sin(f/33)};
 if(f<unfold-60)return opening;
 if(f<unfold+30)return bezier({x:1430,y:550+10*Math.sin((unfold-60)/33)},{x:1410,y:900},{x:300,y:840},N.source,prog(f,unfold-60,unfold+30));
 if(f<launch)return N.source;
 if(f<router)return lerp(N.source,N.router,prog(f,launch,router));
 if(f<depart)return N.router;
 if(f<a)return bezier(N.router,{x:860,y:620},{x:860,y:380},N.a,prog(f,depart,a));
 if(f<b)return lerp(N.a,N.b,prog(f,a,b));
 if(f<arrival)return bezier(N.b,{x:1465,y:380},{x:1465,y:620},N.dest,prog(f,b,arrival));
 if(f<close-60)return N.dest;
 return bezier(N.dest,{x:1610,y:570},{x:1510,y:550},{x:1430,y:550},prog(f,close-60,close+60));
}
export function heroMetrics(f:number){
 const p=hero(f),a=hero(f-.5),b=hero(f+.5);
 const vx=b.x-a.x,vy=b.y-a.y,speed=Math.hypot(vx,vy);
 const radius=mix(96,25,prog(f,event('unfold')-75,event('unfold')+25))+71*prog(f,event('close')-50,event('close')+70);
 const settle=impulse(f,event('arrival'),.15,.09,.35);
 const stretch=1+Math.min(.26,speed*.017)+settle;
 return {...p,radius,angle:Math.atan2(vy,vx)*180/Math.PI,speed,sx:stretch,sy:1/stretch};
}
