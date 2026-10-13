import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import T from '../public/timeline.json';
const C={paper:'#FDFBF7',green:'#1A4A3A',muted:'#426454',gold:'#80601B',yellow:'#E5C158',pale:'#F6EDCF',line:'#CDD5CC'};
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const ease=(v:number)=>{v=clamp(v);return v*v*(3-2*v)};
const show=(t:number,s=0,d=.8)=>ease((t-s)/d);
const txt=(x:number,y:number,text:string,size=36,fill=C.green,anchor='start',weight=400)=><text x={x} y={y} fontSize={size} fill={fill} textAnchor={anchor as any} fontWeight={weight}>{text}</text>;
const line=(d:string,p=1,color=C.line,width=4,dashed=false)=><path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={dashed?'.014 .015':'1'} strokeDashoffset={dashed?0:1-clamp(p)}/>;
function Arrow({x,y,rot=0,color=C.green}:{x:number;y:number;rot?:number;color?:string}){return <path d="M-12 -9 L0 0 L-12 9" fill="none" stroke={color} strokeWidth="3" transform={`translate(${x},${y}) rotate(${rot})`}/>}
function Chip({x,y,s=1,active=true}:{x:number;y:number;s?:number;active?:boolean}){const col=active?C.green:C.line;return <g transform={`translate(${x},${y}) scale(${s})`}>
 <rect x="-49" y="-49" width="98" height="98" rx="4" fill={C.paper} stroke={col} strokeWidth="3"/>
 <rect x="-31" y="-31" width="62" height="62" fill={active?C.pale:C.paper} stroke={col} strokeWidth="1.5"/>
 {[-27,-9,9,27].map((q)=><g key={q} stroke={col} strokeWidth="3"><path d={`M${q} -62V-49 M${q} 49V62 M-62 ${q}H-49 M49 ${q}H62`}/></g>)}
 {[-13,0,13].map((a)=><circle key={a} cx={a} cy={0} r="3" fill={C.gold}/>)}
 </g>}
function Flow({t,closed=true,checkpoint=false}:{t:number;closed?:boolean;checkpoint?:boolean}){
 const nodes=[{x:430,y:415,label:'AI research team'},{x:1450,y:415,label:'Experiments + evaluation'},{x:1450,y:720,label:'Better successor'},{x:430,y:720,label:checkpoint?'Deployment checkpoint':'More useful research capacity'}];
 const paths=['M510 415H1320','M1450 475V650','M1320 720H560','M430 650V490'];
 return <g>
 {paths.map((d,i)=><g key={d} opacity={show(t,i*.65)}>{line(d,show(t,i*.65,.9),i===3?C.gold:C.line,4)}<Arrow x={[1320,1450,560,430][i]} y={[415,650,720,490][i]} rot={[0,90,180,-90][i]} color={i===3?C.gold:C.green}/></g>)}
 {nodes.map((n,i)=><g key={n.label} opacity={show(t,i*.65)}>
 {i===0||i===2?<Chip x={n.x} y={n.y} s={i===2?1.02:.9}/>:i===1?<g transform={`translate(${n.x-61} ${n.y-37})`}>
 {[0,1,2].map(k=><g key={k}><path d={`M${k*49} 0V58Q${k*49} 77 ${k*49+24} 58V0`} fill="none" stroke={C.green} strokeWidth="3"/><path d={`M${k*49+1} ${30+k*8}V55Q${k*49+1} 70 ${k*49+23} 55V${30+k*8}`} fill={C.pale}/></g>)}
 </g>:checkpoint?<g><path d={`M${n.x-58} ${n.y}H${n.x+58}`} stroke={C.gold} strokeWidth="4"/><path d={`M${n.x-35} ${n.y-30}V${n.y+30} M${n.x+35} ${n.y-30}V${n.y+30}`} stroke={C.gold} strokeWidth="5"/></g>:<g>{Array.from({length:15},(_,k)=><rect key={k} x={n.x-60+k%5*27} y={n.y-29+Math.floor(k/5)*27} width="17" height="17" fill={k<Math.floor(4+11*show(t,5,8))?C.green:C.line}/>)}</g>}
 {txt(n.x,n.y+(i<2?-100:105),n.label,32,C.green,'middle',500)}
 </g>)}
 {closed&&t>3&&Array.from({length:5},(_,i)=>{let q=((t-3)*(.08+.009*Math.min(t,14))+i*.2)%1; const a=q*4;let x,y;if(a<1){x=510+810*a;y=415}else if(a<2){x=1450;y=475+175*(a-1)}else if(a<3){x=1320-760*(a-2);y=720}else{x=430;y=650-160*(a-3)}return <circle key={i} cx={x} cy={y} r="7" fill={C.gold} opacity={checkpoint&&a>2.72?.25:.9}/>})}
 {checkpoint&&<g opacity={show(t,5)}>{txt(940,568,'Evidence → decision → access',38,C.gold,'middle',500)}{txt(940,625,'A deliberate checkpoint at every cycle',27,C.muted,'middle')}</g>}
 </g>
}
function Scene({id,t,dur}:{id:string;t:number;dur:number}){
 if(id==='question')return <g>
 <g opacity={show(t,.2)}>{txt(133,493,'A model helps build',47,C.green,'start',400)}{txt(133,555,'its own successor.',47,C.green,'start',400)}{txt(133,658,'What happens when the cycle speeds up?',31,C.muted)}</g>
 <g transform={`translate(1400 545) rotate(${12*show(t,2,8)})`}>
 <circle r="221" fill="none" stroke={C.line} strokeWidth="3"/>
 <path d="M-160 -154 A222 222 0 0 1 195 105" fill="none" stroke={C.gold} strokeWidth="4"/>
 <Arrow x={195} y={105} rot={120} color={C.gold}/>
 {Array.from({length:6},(_,i)=>{const a=i*Math.PI/3+t*.12;return <circle key={i} cx={221*Math.cos(a)} cy={221*Math.sin(a)} r="8" fill={i===0?C.gold:C.green}/>})}
 <Chip x={0} y={0} s={1.9}/></g>
 </g>;
 if(id==='evidence')return <g>
 {[{x:135,num:'>80%',title:'Approved code written by AI',date:'By May 2026',p:.82},{x:1040,num:'26%',title:'R&D work completed autonomously',date:'By August 2026',p:.26}].map((a,i)=><g key={a.num} opacity={show(t,i?10:1)}>
 {txt(a.x,487,a.num,140,i?C.gold:C.green,'start',500)}{txt(a.x,563,a.title,31,C.green,'start',500)}{txt(a.x,614,a.date,28,C.muted)}
 {line(`M${a.x} 678h710`,1,C.line,12)}{line(`M${a.x} 678h${710*a.p}`,show(t,i?11:2,2),i?C.gold:C.green,12)}
 {i===1&&txt(a.x,744,'With high-level human supervision',26,C.muted)}
 </g>)}
 <g opacity={show(t,dur-6)}>{txt(136,817,'Different denominators. Different dates. Not interchangeable.',32,C.gold,'start',500)}</g>
 {txt(136,329,'Anthropic figures cited in the paper',27,C.muted)}
 </g>;
 if(id==='pipeline')return <g>
 {['Idea','Implementation','Experiment','Evaluation'].map((label,i)=>{const x=292+i*438;return <g key={label} opacity={show(t,i*2)}>
 {txt(x,400,String(i+1).padStart(2,'0'),26,C.gold,'middle',500)}
 {i<3&&<g>{line(`M${x+95} 553H${x+339}`,show(t,i*2+.5,1.1),C.line,4)}<Arrow x={x+339} y={553}/></g>}
 {i===0?<g><circle cx={x} cy="533" r="40" stroke={C.green} strokeWidth="3" fill="none"/><path d={`M${x-18} 573V593H${x+18}V573 M${x-11} 608H${x+11}`} stroke={C.green} strokeWidth="3" fill="none"/></g>:i===1?<g>{txt(x,582,'{  }',85,C.green,'middle',400)}</g>:i===2?<g>{[0,1,2].map(k=><rect key={k} x={x-51+k*36} y={595-(30+k*25)*show(t,5,3)} width="23" height={(30+k*25)*show(t,5,3)} fill={k===2?C.gold:C.green}/>)}</g>:<g><circle cx={x-12} cy="540" r="38" stroke={C.green} strokeWidth="3" fill="none"/><path d={`M${x+18} 570L${x+52} 604`} stroke={C.green} strokeWidth="5"/></g>}
 {txt(x,690,label,32,C.green,'middle',500)}
 </g>})}
 <g opacity={show(t,8)}>{txt(960,808,'An improvement has to survive the whole cycle.',36,C.gold,'middle',500)}</g>
 </g>;
 if(id==='loop')return <Flow t={t}/>;
 if(id==='condition'){
 const curves=[{label:'r < 1',note:'Progress slows',color:C.muted,fn:(x:number)=>.1+.4*(1-Math.exp(-4*x))},{label:'r = 1',note:'Pace holds steady',color:C.green,fn:(x:number)=>.1+.58*x},{label:'r > 1',note:'Pace accelerates',color:C.gold,fn:(x:number)=>.1+.74*x*x*x}];
 return <g>
 {curves.map((c,i)=>{const x0=160+i*595,base=715,w=440,h=290;const p=show(t,i*2+1,5);const path=Array.from({length:70},(_,j)=>{let x=j/69*p;return `${j?'L':'M'}${x0+x*w} ${base-h*c.fn(x)}`}).join(' ');return <g key={c.label} opacity={show(t,i*2)}>
 {line(`M${x0} 365V${base}H${x0+w}`,1,C.line,2)}{line(path,1,c.color,5)}
 {txt(x0,332,c.label,55,c.color,'start',500)}{txt(x0,790,c.note,31,c.color)}{txt(x0+w,base+36,'Time',23,C.muted,'end')}
 </g>})}
 {txt(161,858,'Accumulated progress · illustrative shapes, conditional on the model assumptions',24,C.muted)}
 </g>}
 if(id==='scenario')return <g>
 <g opacity={show(t)}>{txt(133,478,'10×',148,C.green,'start',500)}{txt(136,548,'pace of progress',34,C.green)}
 {txt(136,640,'~1.5 years',73,C.gold,'start',500)}{txt(140,701,'after full automation',32,C.gold)}</g>
 <g opacity={show(t,3)}>{line('M790 349V771',1,C.line,2)}{txt(886,383,'Only if:',31,C.muted)}
 {['AI R&D is fully automated','Returns stay at r = 1.2–1.9','No other bottlenecks emerge'].map((q,i)=><g key={q} opacity={show(t,5+i*2.5)}>{txt(887,480+i*106,String(i+1).padStart(2,'0'),25,C.gold)}{txt(954,480+i*106,q,35,C.green,'start',500)}</g>)}
 </g>
 <g opacity={show(t,dur-6)}>{txt(960,833,'This clock does not start today.',42,C.gold,'middle',500)}</g>
 </g>;
 if(id==='friction')return <g>
 {['Diminishing returns','Compute + data limits','Hard-to-automate tasks','Time-intensive processes'].map((q,i)=>{const x=140+i*448;const a=show(t,i*2);return <g key={q} opacity={a}>
 {txt(x,380,String(i+1).padStart(2,'0'),27,C.gold)}
 <g>{line(`M${x} 539H${x+302}`,1,C.line,3)}<path d={`M${x+195} 460V620 M${x+218} 460V620`} stroke={C.green} strokeWidth="5"/>
 {Array.from({length:6},(_,k)=>{let p=(t*.13+k*.15)%1;return <circle key={k} cx={x+Math.min(p*330,175-k*9)} cy={538} r="6" fill={C.gold}/>})}
 <Arrow x={x+302} y={539} color={C.muted}/></g>
 {q.split(' ').length>2?<>{txt(x,690,q.substring(0,q.lastIndexOf(' ')),30,C.green,'start',500)}{txt(x,732,q.substring(q.lastIndexOf(' ')+1),30,C.green,'start',500)}</>:txt(x,690,q,30,C.green,'start',500)}
 </g>})}
 <g opacity={show(t,12)}>{txt(960,837,'More proposals ≠ more validated discoveries',39,C.gold,'middle',500)}</g>
 </g>;
 if(id==='stakes')return <g>
 {line('M960 310V825',1,C.line,2)}
 <g opacity={show(t)}>{txt(139,368,'WHAT COULD ARRIVE SOONER',25,C.muted)}{txt(138,474,'Scientific progress',53,C.green,'start',500)}{txt(138,560,'Medical advances',53,C.green,'start',500)}
 <path d="M142 742 C340 742 390 644 728 644" fill="none" stroke={C.green} strokeWidth="4"/><Arrow x={728} y={644}/>
 {Array.from({length:4},(_,i)=>{let p=(t*.09+i*.25)%1;return <circle key={i} cx={142+586*p} cy={742-98*ease(p)} r="7" fill={C.gold}/>})}</g>
 <g opacity={show(t,4)}>{txt(1056,368,'WHAT COULD FALL BEHIND',25,C.muted)}
 {['Evaluation and adaptation','Human oversight','Checks on power'].map((q,i)=><g key={q} opacity={show(t,4+i*2)}>{txt(1056,478+i*118,q,39,C.gold,'start',500)}{line(`M1056 ${514+i*118}H1737`,1,C.line,2)}</g>)}
 </g>
 </g>;
 if(id==='control')return <Flow t={t} checkpoint/>;
 return <g>
 {['Measure','Constrain','Prepare'].map((q,i)=><g key={q} opacity={show(t,i*2)}>
 {txt(144+i*600,408,String(i+1).padStart(2,'0'),28,C.gold)}{txt(139+i*600,512,q,74,C.green,'start',500)}
 {line(`M${144+i*600} ${560}h${440}`,show(t,i*2+.5,1.3),C.gold,3)}
 {(i===0?['Useful research output','Remaining bottlenecks']:i===1?['Evaluation and oversight','Options to pause workloads']:['Institutions and response','Time to adapt']).map((l,j)=>txt(144+i*600,636+j*55,l,30,C.muted))}
 </g>)}
 <g opacity={show(t,8)}>{txt(960,808,'Track the whole loop.',51,C.gold,'middle',500)}</g>
 </g>
}
export function Film(){
 const f=useCurrentFrame();let idx=T.shots.findIndex(s=>f>=s.start&&f<s.end);if(idx<0)idx=T.shots.length-1;const s=T.shots[idx];const t=(f-s.start)/T.fps;const dur=(s.end-s.start)/T.fps;const alpha=show(t,0,.5)*(1-show(t,dur-.4,.4));const cap=T.captions.find(c=>f>=c.start&&f<c.end);
 const titleSize=s.id==='evidence'?62:70;
 return <AbsoluteFill style={{background:C.paper,fontFamily:'Geist, sans-serif',color:C.green}}>
 <style>{`@font-face{font-family:Geist;src:url('${staticFile('Geist-Regular.woff2')}');font-weight:400}@font-face{font-family:Geist;src:url('${staticFile('Geist-Medium.woff2')}');font-weight:500}@font-face{font-family:Geist;src:url('${staticFile('Geist-SemiBold.woff2')}');font-weight:600}`}</style>
 <AbsoluteFill style={{backgroundImage:`url('${staticFile('paper.png')}')`,opacity:.4}}/>
 <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{position:'absolute',inset:0}}>
 {txt(133,79,'AI RESEARCH / THE FEEDBACK LOOP',24,C.muted)}{txt(1783,79,String(idx+1).padStart(2,'0')+' / 10',24,C.gold,'end')}
 <g opacity={alpha} transform={`translate(0 ${14*(1-show(t,0,.7))})`}>
 {txt(133,166,s.kicker,22,C.gold,'start',500)}
 {s.title.split('\n').map((l,i)=>txt(129,255+i*81,l,titleSize,C.green,'start',500))}
 <Scene id={s.id} t={t} dur={dur}/>
 </g>
 {line('M132 903H1788',1,C.line,1)}
 <path d={`M132 1042H${132+1656*f/T.duration_frames}`} fill="none" stroke={C.gold} strokeWidth="2"/>
 {txt(133,1021,'LeoGuoLabs',24,C.muted)}
 {txt(1786,1021,'WHEN AI BECOMES THE RESEARCH TEAM',19,C.muted,'end')}
 </svg>
 {cap&&<div style={{position:'absolute',top:929,left:200,width:1520,textAlign:'center',fontSize:36,lineHeight:1.28,fontWeight:400}}>{cap.text}</div>}
 {T.shots.map(s=><Sequence key={s.id} from={s.voiceStart}><Audio src={staticFile(s.voice)} volume={1}/></Sequence>)}
 </AbsoluteFill>
}
