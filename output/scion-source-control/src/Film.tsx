import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import T from '../public/timeline.json';

const C={paper:'#FDFBF7',green:'#1A4A3A',muted:'#426454',gold:'#80601B',yellow:'#E5C158',pale:'#F6EDCF',line:'#CBD4C9'};
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>{n=clamp(n);return n*n*(3-2*n)};
const reveal=(t:number,start=0,d=.8)=>ease((t-start)/d);
const text=(x:number,y:number,s:string,size=34,color=C.green,anchor='start',weight=400)=><text x={x} y={y} fontSize={size} fill={color} textAnchor={anchor as any} fontWeight={weight}>{s}</text>;
const rule=(x1:number,y1:number,x2:number,y2:number,color=C.line,w=3)=><line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={w}/>;
const ev=(s:any,id:string,fallback:number)=>s.cues?.[id]!==undefined?(s.cues[id]-s.start)/T.fps:fallback;
function Arrow({x1,y1,x2,y2,p=1,color=C.green,dash=false}:{x1:number;y1:number;x2:number;y2:number;p?:number;color?:string;dash?:boolean}){
 const x=x1+(x2-x1)*clamp(p),y=y1+(y2-y1)*clamp(p),angle=Math.atan2(y2-y1,x2-x1)*180/Math.PI;
 return <g opacity={p>0?1:0}><path d={`M${x1} ${y1}L${x} ${y}`} stroke={color} strokeWidth="3" strokeDasharray={dash?'8 10':undefined}/><path d="M-12 -8L0 0L-12 8" fill="none" stroke={color} strokeWidth="3" transform={`translate(${x},${y}) rotate(${angle})`}/></g>
}
function File({x,y,scale=1,active=false,label=''}:{x:number;y:number;scale?:number;active?:boolean;label?:string}){return <g transform={`translate(${x},${y}) scale(${scale})`}>
 <path d="M-34 -44H15L34 -25V44H-34Z M15 -44V-25H34" fill={active?C.pale:C.paper} stroke={active?C.gold:C.green} strokeWidth="2.5"/>
 {[-7,7,21].map((q,i)=><path key={i} d={`M-20 ${q}H${i===2?4:20}`} stroke={active?C.gold:C.muted} strokeWidth="2"/>)}
 {label&&text(0,73,label,22,C.muted,'middle')}
 </g>}
function Server({x,y,label='Source service',scale=1}:{x:number;y:number;label?:string;scale?:number}){return <g transform={`translate(${x},${y}) scale(${scale})`}>
 {[0,1,2].map(i=><g key={i}><rect x="-76" y={-78+i*53} width="152" height="42" fill={C.paper} stroke={C.green} strokeWidth="2.5"/>{rule(-48,-57+i*53,29,-57+i*53,C.line,3)}<circle cx="52" cy={-57+i*53} r="4" fill={C.gold}/></g>)}
 {text(0,126,label,26,C.green,'middle',500)}</g>}
function Laptop({x,y,label='Workspace'}:{x:number;y:number;label?:string}){return <g transform={`translate(${x},${y})`}>
 <rect x="-110" y="-77" width="220" height="144" fill={C.paper} stroke={C.green} strokeWidth="3"/>
 <path d="M-110 67L-138 87H138L110 67 M-40 87H40" fill="none" stroke={C.green} strokeWidth="3"/>
 {text(0,137,label,28,C.green,'middle',500)}</g>}
function ObjectGrid({x,y,active=-1,count=20,small=false}:{x:number;y:number;active?:number;count?:number;small?:boolean}){let size=small?19:31,gap=small?28:45;return <g>{Array.from({length:count},(_,i)=><rect key={i} x={x+i%5*gap} y={y+Math.floor(i/5)*gap} width={size} height={size} fill={i===active?C.yellow:C.paper} stroke={i===active?C.gold:C.green} strokeWidth="2"/>)}</g>}

function Scene({s,t,dur}:{s:any;t:number;dur:number}){
 if(s.id==='bottleneck'){
  const q=reveal(t,ev(s,'growth',4),2);return <g>
  <g opacity={reveal(t,.4)}>{text(150,475,'2,500',108,C.green,'start',500)}{text(152,526,'May 2026',28,C.muted)}{rule(153,570,214,570,C.green,16)}</g>
  <g opacity={q}>{text(1030,475,'>30,000',108,C.gold,'start',500)}{text(1035,526,'September 2026',28,C.muted)}{rule(1035,570,1035+730*q,570,C.gold,16)}</g>
  {text(151,653,'Code changes merged per day · reported by Anthropic',27,C.muted)}
  <g opacity={reveal(t,ev(s,'downstream',12))}>{text(153,785,'Write',31,C.green,'start',500)}<Arrow x1={300} y1={775} x2={800} y2={775} color={C.line}/>
  {Array.from({length:13},(_,i)=><rect key={i} x={Math.min(330+(t%7)*100+i*32,760-i*25)} y={762} width="17" height="26" fill={C.green}/>)}
  {rule(826,732,826,817,C.gold,6)}{rule(846,732,846,817,C.gold,6)}
  {text(923,785,'Retrieve → build → test → review',36,C.gold,'start',500)}</g>
  </g>;
 }
 if(s.id==='git'){
  const offline=reveal(t,ev(s,'offline',9),1),move=reveal(t,2,2);
  return <g><Server x={363} y={560} label="Shared repository"/>
  <g opacity={1-offline*.75}><Arrow x1={510} y1={555} x2={1180} y2={555} p={move} color={C.line}/><File x={550+560*move} y={555} scale={.7}/></g>
  <Laptop x={1390} y={561} label="Local repository"/><ObjectGrid x={1323} y={522} count={10} small/>
  <g opacity={reveal(t,3)}>{text(1390,805,'History · diffs · local commits',30,C.green,'middle',500)}
  {rule(1110,734,1668,734,C.line,2)}{Array.from({length:7},(_,i)=><circle key={i} cx={1110+i*93} cy="734" r="7" fill={i===6?C.gold:C.green}/>)}</g>
  <g opacity={offline}>{rule(815,535,853,573,C.gold,4)}{rule(853,535,815,573,C.gold,4)}{text(833,630,'Offline',29,C.gold,'middle',500)}</g>
  {text(364,802,'A workshop with its own library',28,C.muted,'middle')}
  </g>;
 }
 if(s.id==='partial'){
  const starts=[ev(s,'shallow',4),ev(s,'partial',7),ev(s,'sparse',11)];
  return <g>{['Shallow clone','Partial clone','Sparse checkout'].map((label,i)=>{let x=145+i*594,p=reveal(t,starts[i]);return <g key={label} opacity={.18+.82*p}>
   {text(x,438,label,40,C.green,'start',500)}
   {i===0?<g>{rule(x+15,573,x+440,573,C.line,3)}{Array.from({length:8},(_,k)=><circle key={k} cx={x+15+k*58} cy="573" r="13" fill={k<5?C.paper:C.green} stroke={k<5?C.line:C.green} strokeWidth="2"/>)}{text(x,685,'Recent commits',29,C.muted)}</g>:i===1?<g><ObjectGrid x={x+15} y={507} active={7} count={15}/><File x={x+356} y={555} scale={.8} active/>{text(x,685,'Fetch object contents later',29,C.muted)}</g>:<g>
   {rule(x+30,500,x+30,629,C.green,3)}{['/app','/tests','/docs'].map((q,k)=><g key={q}>{rule(x+30,513+k*55,x+91,513+k*55,k===0?C.green:C.line,3)}{text(x+112,523+k*55,q,29,k===0?C.green:C.line,'start',500)}</g>)}{text(x,685,'Choose visible directories',29,C.muted)}</g>}
   {rule(x,731,x+440,731,C.line,2)}{text(x,782,['History depth','Object data','Working tree'][i],31,C.gold,'start',500)}
  </g>})}</g>;
 }
 if(s.id==='contract'){
  const p=reveal(t,ev(s,'server',8),2);return <g>
   <Laptop x={430} y={576} label="Thin client"/><ObjectGrid x={366} y={535} count={10} small/>
   {text(430,799,'Bounded object cache',29,C.muted,'middle')}
   <Arrow x1={610} y1={548} x2={1210} y2={548} p={reveal(t,1,2)} color={C.gold}/><Arrow x1={1210} y1={611} x2={610} y2={611} p={reveal(t,3,2)} color={C.green}/>
   {text(914,479,'Reachable service',28,C.gold,'middle',500)}<Server x={1430} y={573} label="Scion server"/>
   <g opacity={p}>{text(1430,779,'History · merge · commit',30,C.green,'middle',500)}</g>
  </g>;
 }
 if(s.id==='demand'){
  const local=ev(s,'locally',5),miss=ev(s,'upstream',10),arrival=ev(s,'appears',12),repeat=ev(s,'reuse',16);
  const p1=reveal(t,miss,1.5),p2=reveal(t,arrival,1.5),p3=reveal(t,repeat,1.4);
  return <g><Laptop x={320} y={570} label="Test workspace"/>
   <g><rect x="820" y="489" width="248" height="164" fill={C.paper} stroke={C.green} strokeWidth="3"/><ObjectGrid x={848} y={514} count={15} small/><g opacity={p1}><File x={1022} y={578} scale={.6} active/></g>{text(944,710,'Local cache',29,C.green,'middle',500)}</g>
   <Server x={1570} y={570} label="Upstream objects"/>
   <Arrow x1={480} y1={480} x2={790} y2={480} p={reveal(t,local,1)} color={C.line}/>
   <Arrow x1={1110} y1={480} x2={1450} y2={480} p={p1} color={C.line}/>
   <g opacity={p1*(1-p2)}><File x={1470-400*p1} y={600} scale={.6} active/></g>
   <Arrow x1={802} y1={600} x2={473} y2={600} p={p2} color={C.gold}/>
   {p2>0&&<File x={790-470*p2} y={570} active scale={.7}/>}
   <g opacity={p3}><Arrow x1={802} y1={775} x2={473} y2={775} p={p3} color={C.gold}/>{text(1170,789,'Next request: reuse nearby',31,C.gold,'middle',500)}</g>
   {text(320,826,'parser.ts',29,C.gold,'middle',500)}{text(1570,823,'Conceptual example',24,C.muted,'middle')}
  </g>;
 }
 if(s.id==='api'){
  const p=reveal(t,ev(s,'changeset',10));return <g>
   {text(290,431,'Job',30,C.green,'middle',500)}{text(1510,431,'Source service',30,C.green,'middle',500)}
   <Arrow x1={440} y1={473} x2={1350} y2={473} p={reveal(t,1,2)} color={C.green}/>{text(900,444,'“What changed?”',30,C.muted,'middle')}
   <Arrow x1={1350} y1={547} x2={440} y2={547} p={reveal(t,4,2)} color={C.gold}/>{text(900,596,'A diff, without a working copy',31,C.gold,'middle',500)}
   <g opacity={p}>{rule(146,650,1770,650,C.line,1)}
    {text(170,713,'Changeset',36,C.green,'start',500)}{text(170,766,'/src/parser.ts',27,C.muted)}{text(170,813,'/tests/parser.test.ts',27,C.muted)}
    <Arrow x1={680} y1={757} x2={1110} y2={757} p={reveal(t,ev(s,'content',13),1.3)} color={C.line}/>
    <File x={1240} y={756} active scale={.8}/><File x={1390} y={756} scale={.8}/>{text(1570,764,'File data',30,C.green,'middle',500)}
   </g>
  </g>;
 }
 if(s.id==='cache'){
  const xs=[266,720,1174,1628];let p=reveal(t,1,4),r=reveal(t,ev(s,'reuse',10),6);
  return <g>{xs.map((x,i)=><g key={i} opacity={reveal(t,i*.45)}>
    {i<3&&<Arrow x1={x+113} y1={516} x2={x+330} y2={516} p={clamp(p*3-i)} color={C.line}/>}
    {i===0?<Laptop x={x} y={578} label="Job"/>:i===3?<Server x={x} y={578} label="Source server"/>:<g><rect x={x-94} y="500" width="188" height="155" fill={C.paper} stroke={C.green} strokeWidth="3"/><ObjectGrid x={x-67} y={521} small count={15} active={7}/>{text(x,710,i===1?'Node cache':'Regional cache',29,C.green,'middle',500)}</g>}
   </g>)}
   {Array.from({length:3},(_,i)=><g key={i} opacity={reveal(t,4+i*.8)}><Arrow x1={xs[3-i]-119} y1={618} x2={xs[2-i]+120} y2={618} p={reveal(t,4+i*.8,.8)} color={C.gold}/></g>)}
   <g opacity={r}>{text(959,805,'One immutable object. Many readers.',38,C.gold,'middle',500)}</g>
   {t>ev(s,'reuse',10)&&<File x={590-((t-ev(s,'reuse',10))%3)/3*190} y={617} scale={.36} active/>}
  </g>;
 }
 if(s.id==='results')return <g>
   <g opacity={reveal(t,.4)}>{text(150,565,'200×',145,C.green,'start',500)}{text(156,637,'smaller CPU + memory footprint',33,C.green,'start',500)}{text(156,689,'Source-control infrastructure',28,C.muted)}</g>
   {rule(985,406,985,783,C.line,2)}
   <g opacity={reveal(t,ev(s,'ci',7))}>{text(1110,565,'25%',145,C.gold,'start',500)}{text(1118,637,'CPU capacity gain',33,C.green,'start',500)}{text(1118,689,'Continuous integration',28,C.muted)}</g>
   {text(156,825,'Anthropic’s workload · company-reported results',28,C.muted)}
  </g>;
 if(s.id==='tradeoff'){
  return <g>
   <g opacity={reveal(t,.4)}>{text(151,445,'Local independence',41,C.green,'start',500)}{text(151,506,'Useful when the network disappears',28,C.muted)}<Laptop x={390} y={661} label="Keep working locally"/></g>
   <g opacity={reveal(t,3)}>{text(1066,445,'Shared online services',41,C.green,'start',500)}{text(1066,506,'Useful when work stays connected',28,C.muted)}<Server x={1300} y={661} label="Depend on service availability"/></g>
   {rule(925,402,925,810,C.line,2)}
   <g opacity={reveal(t,ev(s,'questions',10))}>{text(960,864,'What stays local?  What is shared?  What happens offline?',32,C.gold,'middle',500)}</g>
  </g>;
 }
 const labels=['Write','Retrieve','Build','Test','Review'];const active=Math.floor((t/2.7)%5);
 return <g>
  {labels.map((label,i)=>{let x=260+i*350;return <g key={label} opacity={reveal(t,i*.3)}>
   {text(x,473,String(i+1).padStart(2,'0'),25,C.gold,'middle')}
   <circle cx={x} cy="563" r="45" fill={i===active?C.pale:C.paper} stroke={i===active?C.gold:C.line} strokeWidth="3"/>
   {i===0?text(x,576,'{ }',36,C.green,'middle',500):i===1?<File x={x} y={564} active={i===active} scale={.5}/>:<path d={i===2?`M${x-15} 580V550H${x+15}V580Z`:i===3?`M${x-20} 561L${x-3} 577L${x+22} 548`:`M${x-18} 553H${x+18}M${x-18} 565H${x+18}M${x-18} 577H${x+3}`} fill="none" stroke={C.green} strokeWidth="3"/>}
   {i<4&&<Arrow x1={x+63} y1={563} x2={x+278} y2={563} color={C.line}/>}{text(x,665,label,35,C.green,'middle',500)}
  </g>})}
  <g opacity={reveal(t,ev(s,'lesson',11))}>{text(960,791,'Move less. Reuse more.',66,C.gold,'middle',500)}{text(960,850,'Give each operation only the work it needs.',31,C.muted,'middle')}</g>
 </g>;
}

export function Film(){
 const frame=useCurrentFrame();let idx=T.shots.findIndex(s=>frame>=s.start&&frame<s.end);if(idx<0)idx=T.shots.length-1;
 const s=T.shots[idx],t=(frame-s.start)/T.fps,dur=(s.end-s.start)/T.fps;
 const opacity=reveal(t,0,.4)*(idx===T.shots.length-1?1:1-reveal(t,dur-.3,.3));
 const caption=T.captions.find(c=>frame>=c.start&&frame<c.end);
 return <AbsoluteFill style={{background:C.paper,fontFamily:'Geist, sans-serif',color:C.green}}>
  <style>{`@font-face{font-family:Geist;src:url('${staticFile('Geist-Regular.woff2')}');font-weight:400}@font-face{font-family:Geist;src:url('${staticFile('Geist-Medium.woff2')}');font-weight:500}@font-face{font-family:Geist;src:url('${staticFile('Geist-SemiBold.woff2')}');font-weight:600}`}</style>
  <AbsoluteFill style={{backgroundImage:`url('${staticFile('paper.png')}')`,opacity:.3}}/>
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{position:'absolute',inset:0}}>
   {text(132,80,'SCION / SOURCE CONTROL AT AGENT SCALE',23,C.muted)}{text(1788,80,`${String(idx+1).padStart(2,'0')} / 10`,24,C.gold,'end')}
   <g opacity={opacity}>
    {text(134,158,s.kicker,22,C.gold,'start',500)}
    {s.title.split('\n').map((l,i)=>text(129,239+i*77,l,69,C.green,'start',500))}
    <Scene s={s} t={t} dur={dur}/>
   </g>
   {rule(132,904,1788,904,C.line,1)}{rule(132,1043,132+1656*(frame+1)/T.duration_frames,1043,C.gold,2)}
   {text(132,1021,'LeoGuoLabs',24,C.muted)}{text(1788,1021,'WHEN CODE OUTRUNS THE PLUMBING',19,C.muted,'end')}
  </svg>
  {caption&&<div style={{position:'absolute',left:195,top:927,width:1530,fontSize:35,lineHeight:1.3,textAlign:'center'}}>{caption.text}</div>}
  {T.shots.map(s=><Sequence key={s.id} from={s.voiceStart}><Audio src={staticFile(s.voice)} volume={1}/></Sequence>)}
  {T.shots.map(s=><Sequence key={s.id+'-cue'} from={s.start}><Audio src={staticFile('transition.wav')} volume={.38}/></Sequence>)}
 </AbsoluteFill>;
}
