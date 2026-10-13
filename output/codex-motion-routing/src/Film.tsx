import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame} from 'remotion';
import {T,N,event,clamp,ease,prog,mix,impulse,hero,heroMetrics} from './motion';
const C={paper:'#FDFBF7',green:'#1A4A3A',muted:'#426454',gold:'#80601B',bright:'#E5C158',line:'#CED5C9'};
const font='Geist, sans-serif';
const enter=(f:number,s:number)=>prog(f,s,s+25);
const exit=(f:number,e:number)=>1-prog(f,e-22,e);
function Caption({f,start,end,top=180,children,small}:{f:number;start:number;end:number;top?:number;children:React.ReactNode;small?:string}){
 const a=enter(f,start)*exit(f,end);
 return <g opacity={a} transform={`translate(0,${18*(1-enter(f,start))})`}>
   <text x="136" y={top} fill={C.green} fontSize="78" fontWeight="500" letterSpacing="-3">{children}</text>
   {small&&<text x="140" y={top+65} fill={C.muted} fontSize="30" fontWeight="400">{small}</text>}
 </g>;
}
function Ring({f,at,x,y,color=C.gold,max=85}:{f:number;at:number;x:number;y:number;color?:string;max?:number}){
 const q=clamp((f-at)/42);if(f<at||q>=1)return null;
 return <circle cx={x} cy={y} r={28+max*ease(q)} fill="none" stroke={color} strokeWidth={3*(1-q)+.5} opacity={.65*(1-q)}/>;
}
function Path({d,p=1,color=C.line,width=4,opacity=1,dashed=false}:{d:string;p?:number;color?:string;width?:number;opacity?:number;dashed?:boolean}){
 return <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" opacity={opacity} pathLength="1" strokeDasharray={dashed?'.009 .012':'1'} strokeDashoffset={dashed?0:1-clamp(p)}/>;
}
export function Film({silent=false}:{silent?:boolean}){
 const f=useCurrentFrame();const h=heroMetrics(f);
 const net=prog(f,172,250)*(1-prog(f,1180,1270));
 const broken=prog(f,event('break'),event('break')+18);
 const alt=prog(f,event('alternate'),event('alternate')+100);
 const intro=1-prog(f,143,205),outro=prog(f,1200,1270);
 const orbitOpacity=Math.max(intro,outro);
 const cableA=impulse(f,event('break'),36,.038,.21),cableB=impulse(f,event('break')+5,-31,.042,.19);
 const short='M320 620 L780 620';
 const upperA='M780 620 C860 620 860 380 1000 380';
 const upperB='M1000 380 L1320 380';
 const upperC='M1320 380 C1465 380 1465 620 1610 620';
 const dlow='M780 620 C880 620 920 830 1110 830 C1390 830 1430 620 1610 620';
 const inset=14*Math.sin((f-175)/45)*(1-prog(f,175,300));
 return <AbsoluteFill style={{background:C.paper,fontFamily:font}}>
  <style>{`@font-face{font-family:Geist;src:url('${staticFile('Geist-Regular.woff2')}')}@font-face{font-family:Geist;src:url('${staticFile('Geist-Medium.woff2')}');font-weight:500}@font-face{font-family:Geist;src:url('${staticFile('Geist-SemiBold.woff2')}');font-weight:600}`}</style>
  <AbsoluteFill style={{backgroundImage:`url('${staticFile('paper.png')}')`,opacity:.45}}/>
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{fontFamily:font,position:'absolute',inset:0}}>
   <text x="138" y="75" fontSize="23" fill={C.muted} letterSpacing="3">NETWORKS IN MOTION</text>
   <text x="1782" y="75" fontSize="23" textAnchor="end" fill={C.gold}>01</text>
   <g opacity={intro}>
    <g opacity={enter(f,4)} transform={`translate(0,${24*(1-enter(f,4))})`}>
     <text x="136" y="398" fontSize="108" fontWeight="500" fill={C.green} letterSpacing="-5">A route</text>
    </g>
    <g opacity={enter(f,22)} transform={`translate(0,${24*(1-enter(f,22))})`}>
     <text x="136" y="520" fontSize="108" fontWeight="500" fill={C.green} letterSpacing="-5">around failure.</text>
    </g>
    <text x="141" y="619" fontSize="32" fill={C.muted} opacity={enter(f,52)}>One packet. More than one way through.</text>
    <path d="M140 688 L228 688" stroke={C.gold} strokeWidth="3" pathLength="1" strokeDasharray="1" strokeDashoffset={1-enter(f,68)}/>
   </g>
   <g opacity={orbitOpacity*enter(f,18)} transform={`translate(1430 550) rotate(${f*.10})`}>
    {[205,250,295].map((r,i)=><g key={r} opacity={1-i*.24}>
      <ellipse rx={r} ry={r*.70} transform={`rotate(${i*48-32})`} fill="none" stroke={i===0?C.green:C.line} strokeWidth={i===0?3:2}/>
      <circle cx={r*Math.cos(f/68+i*2)} cy={r*.7*Math.sin(f/68+i*2)} r={i===0?10:6} fill={i===0?C.green:C.gold} transform={`rotate(${i*48-32})`}/>
    </g>)}
   </g>
   <g opacity={net} transform={`translate(0 ${inset})`}>
    <Path d={dlow} p={prog(f,208,300)} width={3} opacity={.78}/>
    <Path d={upperA} p={prog(f,190,265)} width={3}/>
    <Path d={upperB} p={prog(f,212,290)} width={3}/>
    <Path d={upperC} p={prog(f,230,310)} width={3}/>
    <Path d={short} p={prog(f,187,247)} color={C.green} width={6}/>
    <Path d={`M780 620 C930 620 1060 ${620+cableA} ${mix(1195,1150,broken)} ${620+cableA*.3}`} color={broken>.5?C.line:C.green} width={6} p={prog(f,219,284)}/>
    <Path d={`M${mix(1195,1240,broken)} ${620+cableB*.3} C1390 ${620+cableB} 1460 620 1610 620`} color={broken>.5?C.line:C.green} width={6} p={prog(f,242,314)}/>
    <Path d={upperA} p={clamp(alt*3)} color={C.green} width={6}/>
    <Path d={upperB} p={clamp(alt*3-1)} color={C.green} width={6}/>
    <Path d={upperC} p={clamp(alt*3-2)} color={C.green} width={6}/>
    {Object.entries(N).map(([name,p],i)=>{
     const impact=impulse(f,event('break')+Math.round(Math.abs(p.x-1195)/45)+5,5,.10,.2);
     const pop=prog(f,186+i*8,238+i*8);
     const active=name==='source'||name==='router'||name==='dest'||(alt>.9&&name!=='lower');
     return <g key={name} transform={`translate(${p.x} ${p.y+impact}) scale(${.7+.3*pop})`} opacity={pop}>
      <circle r={name==='dest'?48:36} fill={C.paper} stroke={active?C.green:C.line} strokeWidth={active?3:2}/>
      <circle r={name==='dest'?37:27} fill="none" stroke={active?C.green:C.line} strokeWidth="1" opacity=".45"/>
      {name!=='dest'&&name!=='source'&&<circle r="5" fill={active?C.green:C.line}/>}
     </g>;
    })}
    <text x="320" y="712" textAnchor="middle" fontSize="26" fill={C.muted} opacity={enter(f,260)}>SOURCE</text>
    <text x="780" y="712" textAnchor="middle" fontSize="26" fill={C.muted} opacity={enter(f,280)}>ROUTER</text>
    <text x="1610" y="720" textAnchor="middle" fontSize="26" fill={C.muted} opacity={enter(f,300)}>DESTINATION</text>
    <g opacity={broken*exit(f,1170)}>
     <path d="M1182 608 L1208 634 M1208 608 L1182 634" stroke={C.gold} strokeWidth="4" strokeLinecap="round"/>
     <text x="1195" y="694" textAnchor="middle" fontSize="27" fill={C.gold} opacity={enter(f,event('break')+18)}>LINK DOWN</text>
    </g>
    <text x="1160" y="322" fontSize="26" fill={C.green} textAnchor="middle" opacity={enter(f,event('alternate')+92)*exit(f,1170)}>ALTERNATE ROUTE</text>
    <Ring f={f} at={event('router')} {...N.router}/>
    <Ring f={f} at={event('break')} x={1195} y={620} max={56}/>
    <Ring f={f} at={event('upper-a')} {...N.a}/>
    <Ring f={f} at={event('upper-b')} {...N.b}/>
    <Ring f={f} at={event('arrival')} {...N.dest} max={120}/>
    <Ring f={f} at={event('arrival')+11} {...N.dest} max={85} color={C.green}/>
    <g opacity={enter(f,event('break')+44)*exit(f,event('depart'))} transform={`translate(780 620) rotate(${(f-event('break')-44)*2.4})`}>
     <circle r="53" fill="none" stroke={C.gold} strokeWidth="2.5" pathLength="1" strokeDasharray=".19 .81"/>
    </g>
   </g>
   {f>event('launch')&&f<event('arrival')&&[12,8,4].map((lag,i)=>{
    const p=hero(f-lag);return <circle key={lag} cx={p.x} cy={p.y} r={16+i*2} fill={C.bright} opacity={h.speed>1?.05+i*.04:0}/>;
   })}
   <g transform={`translate(${h.x} ${h.y}) rotate(${h.angle}) scale(${h.sx} ${h.sy})`}>
     <circle r={h.radius*enter(f,5)} fill={C.bright}/>
     <circle r={h.radius*.62*enter(f,18)} fill="none" stroke={C.gold} strokeWidth="2" opacity={mix(.45,0,prog(f,150,220))+.35*outro}/>
     <circle r={4+4*Math.max(intro,outro)} fill={C.gold} opacity={.7}/>
   </g>
   <Caption f={f} start={228} end={440} small="Send the packet toward its destination.">Start with a path.</Caption>
   <Caption f={f} start={event('break')+13} end={680} small="The direct connection is no longer available.">Then a link breaks.</Caption>
   <Caption f={f} start={event('alternate')-5} end={920} small="An available branch provides another way through.">Change the route.</Caption>
   <Caption f={f} start={953} end={1160} small="The path changes. The endpoint stays the same.">Keep the destination.</Caption>
   <g opacity={outro}>
    <text x="136" y="410" fontSize="103" fontWeight="500" letterSpacing="-4.5" fill={C.green}>Another path.</text>
    <text x="136" y="528" fontSize="103" fontWeight="500" letterSpacing="-4.5" fill={C.green}>Same destination.</text>
    <text x="141" y="631" fontSize="32" fill={C.muted} opacity={enter(f,1288)}>Resilience needs an alternative.</text>
    <path d="M140 690 L228 690" stroke={C.gold} strokeWidth="3"/>
   </g>
   <text x="140" y="1004" fontSize="24" fill={C.muted}>A routing metaphor</text>
   <text x="1780" y="1004" fontSize="27" fill={C.green} textAnchor="end">LeoGuoLabs</text>
   <path d="M140 1032 L1780 1032" stroke={C.line} strokeWidth="1"/>
   <path d={`M140 1032 L${140+1640*f/1439} 1032`} stroke={C.gold} strokeWidth="2"/>
  </svg>
  {!silent&&<Audio src={staticFile('soundtrack.wav')}/>}
 </AbsoluteFill>;
}
