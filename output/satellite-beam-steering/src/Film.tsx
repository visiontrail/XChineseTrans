import React,{useLayoutEffect} from 'react';
import {AbsoluteFill,Audio,Img,staticFile,useCurrentFrame} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {Satellite,ArrayPanel,Box,RoundBox,Line3D,Beam,Globe,C} from './Models';
import {ramp,smooth,lerp,thetaAt,phaseStep,arrayFactor,shotAt,pointingState} from './motion';
const titles=[['Steering without turning.','How a satellite points an electronic beam.'],['Start with the aperture.','Many radiating elements. One coordinated array.'],['Look beneath the surface.','A feed network sets the relative phase.'],['Shift phase. Change direction.','The elements stay active. Their waves add differently.'],['The satellite moves.','The beam follows the terminal.'],['One array. A changing direction.','Electronic pointing starts with relative phase.']];
const chapters=['01 / SPACECRAFT','02 / APERTURE','03 / FEED NETWORK','04 / INTERFERENCE','05 / POINTING','06 / THE PRINCIPLE'];
function Camera({position,target,zoom}:any){const {camera,invalidate}=useThree();useLayoutEffect(()=>{camera.position.set(...position);camera.lookAt(...target);(camera as THREE.OrthographicCamera).zoom=zoom;camera.updateProjectionMatrix();invalidate()},[...position,...target,zoom]);return null}
function Lights(){return <><ambientLight intensity={1.8}/><directionalLight position={[3,8,8]} intensity={3.5} color='#fff6df'/><directionalLight position={[-8,0,6]} intensity={1.5} color='#d9e6e1'/><directionalLight position={[0,5,-8]} intensity={2.2}/></>}
function PhasedSlice({t}:any){
 const theta=thetaAt(t),rad=theta*Math.PI/180;
 const pts=Array.from({length:181},(_,i)=>{const a=(i-90)*Math.PI/180,r=4.7*arrayFactor(i-90,theta);return [r*Math.sin(a),0,r*Math.cos(a)]});
 return <group position={[2.0,-.8,0]}>
 <RoundBox s={[4.2,.58,.16]} color={C.metal}/>
 {Array.from({length:8},(_,i)=><group key={i} position={[-1.75+i*.5,0,.12]}>
 <Box s={[.35,.35,.035]} color={C.foil} metal={.65}/>
 <Line3D points={[[0,-.17,.04],[0,-.34,.04],[0,-.45,-.02]]} color={C.gold} width={.013}/>
 </group>)}
 <Line3D points={pts} width={.025} color={C.green}/>
 <Line3D points={Array.from({length:31},(_,i)=>[1.2*Math.sin(rad*i/30),.04,1.2*Math.cos(rad*i/30)])} color={C.gold} width={.01}/>
 <Line3D points={[[0,0,0],[0,0,5.3]]} color='#a7afa1' width={.008}/>
 <Line3D points={[[0,0,0],[Math.sin(rad)*5.2,0,Math.cos(rad)*5.2]]} color={C.gold} width={.019}/>
 {Array.from({length:5},(_,i)=>{const d=.8+((t*1.05+i*.75)%3.8);return <Line3D key={i} points={[[-1.2*Math.cos(rad)+d*Math.sin(rad),.12,1.2*Math.sin(rad)+d*Math.cos(rad)],[1.2*Math.cos(rad)+d*Math.sin(rad),.12,-1.2*Math.sin(rad)+d*Math.cos(rad)]]} color={C.gold} width={.014} opacity={.13+.34*Math.sin((d/4.6)*Math.PI)}/>})}
 </group>
}
function Tracking({t}:any){
 const {x,y,target,from}=pointingState(t);
 return <>
 <Globe radius={10} position={[0,-12.3,0]}/>
 <Line3D points={Array.from({length:41},(_,i)=>[-3.4+i*.17,2.9,0])} color='#afb5a5' width={.012}/>
 <group position={[x,y,0]} rotation={[Math.PI/2,0,0]} scale={.41}><Satellite/></group>
 <Beam from={from} to={target} r={.63} opacity={.08}/>
 <group position={target as any}>
 <mesh rotation={[-Math.PI/2,0,0]}><ringGeometry args={[.55,.575,64]}/><meshBasicMaterial color={C.gold} side={THREE.DoubleSide}/></mesh>
 <RoundBox p={[0,.08,0]} s={[.3,.22,.3]} color={C.green}/>
 <mesh position={[0,.22,0]} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[.18,32]}/><meshStandardMaterial color={C.paper} side={THREE.DoubleSide}/></mesh>
 </group>
 </>
}
function Scene({shot,t}:any){
 let camera:any;
 let content;
 if(shot===0){const p=ramp(t,0,6);camera={position:[lerp(7,5.5,p),lerp(4.5,3.4,p),13],target:[-1.1,.3,0],zoom:lerp(109,121,p)};content=<group position={[1.15,-.25,0]} rotation={[.03,lerp(-.12,.13,p),-.13]}><Satellite/></group>}
 else if(shot===1){const p=ramp(t,0,6);camera={position:[lerp(5.5,2.8,p),lerp(3.4,1.5,p),13],target:[-.72,.05,.3],zoom:lerp(207,237,p)};content=<group position={[1.45,-.15,0]} rotation={[0,.13,-.13]} scale={1.06}><ArrayPanel/></group>}
 else if(shot===2){const p=ramp(t,.5,3.7);camera={position:[7-1.1*ramp(t,0,6),3.6,10],target:[-.9,0,.8],zoom:185};content=<group position={[1.3,-.1,0]} rotation={[0,-.14,-.12]}><ArrayPanel explode={p}/>{[[-1.05,-1.05],[1.05,1.05]].map(([x,y],i)=><Line3D key={i} points={[[x,y,0],[x,y,2.15*p+.3]]} color='#a5afa2' width={.008} opacity={.7}/>)}</group>}
 else if(shot===3){camera={position:[8,8,10],target:[.05,-.7,1.4],zoom:127};content=<PhasedSlice t={t}/>}
 else if(shot===4){camera={position:[7,3.8,12],target:[-.8,1,0],zoom:96};content=<Tracking t={t}/>}
 else {const p=ramp(t,0,6);camera={position:[5.2+1.5*p,2.9+1.0*p,13],target:[-1.1,.3,0],zoom:lerp(122,113,p)};content=<group position={[1.15,-.25,0]} rotation={[.03,.13+.12*p,-.13]}><Satellite/></group>}
 return <ThreeCanvas orthographic width={1920} height={1080} camera={{position:[6,4,13],zoom:120,near:.1,far:200}} gl={{antialias:true,alpha:true}} dpr={1} style={{position:'absolute',inset:0}}><Camera {...camera}/><Lights/>{content}</ThreeCanvas>
}
function PhaseData({t}:any){const a=thetaAt(t),step=phaseStep(a);return <div style={{position:'absolute',left:122,top:390,width:435}}>
 <div style={{fontSize:22,color:C.muted,letterSpacing:1}}>PHASE / FIRST 4 ELEMENTS</div>
 <svg width='420' height='240' viewBox='0 0 420 240'>
 {Array.from({length:4},(_,i)=>{const ph=i*step,base=44+i*52;return <g key={i}><text x='0' y={base+6} fill={C.green} fontSize='22'>{`${Math.round(ph)}°`}</text><path d={Array.from({length:161},(_,j)=>{const x=95+j*1.8,y=base-14*Math.sin(j/160*Math.PI*4+ph*Math.PI/180+t*2*Math.PI);return `${j?'L':'M'}${x},${y}`}).join(' ')} fill='none' stroke={i===0?C.muted:C.gold} strokeWidth='2.3'/></g>})}
 </svg>
 <div style={{fontSize:49,fontWeight:500,letterSpacing:-2}}>{a.toFixed(0)}° <span style={{fontSize:24,letterSpacing:0,color:C.muted}}>beam angle</span></div>
 <div style={{marginTop:12,fontSize:25,color:C.gold}}>Δφ = {step.toFixed(0)}° per element</div>
 <div style={{marginTop:20,fontSize:20,color:C.muted}}>8-element slice · d = λ/2</div>
 </div>}

function projectPoint(local:number[],cameraPosition:number[],target:number[],zoom:number,position=[0,0,0],rotation=[0,0,0]){
 const cam=new THREE.OrthographicCamera(-960,960,540,-540,.1,200);cam.position.set(...cameraPosition as [number,number,number]);cam.lookAt(...target as [number,number,number]);cam.zoom=zoom;cam.updateProjectionMatrix();cam.updateMatrixWorld();
 const v=new THREE.Vector3(...local as [number,number,number]).applyEuler(new THREE.Euler(...rotation as [number,number,number])).add(new THREE.Vector3(...position as [number,number,number])).project(cam);return [(v.x+1)*960,(1-v.y)*540];
}
function GeometryLabels({shot,t}:any){
 if(shot===2){const e=ramp(t,.5,3.7);const pos=[1.3,-.1,0],rot=[0,-.14,-.12],cam=[7-1.1*ramp(t,0,6),3.6,10],target=[-.9,0,.8];return <svg width='1920' height='1080' style={{position:'absolute',inset:0,pointerEvents:'none',opacity:ramp(t,1.2,2.3)}}>{[[.14+e*1.9,'01'],[e*.85,'02'],[-.13,'03']].map(([z,label])=>{const p=projectPoint([-1.25,1.12,Number(z)],cam,target,185,pos,rot);return <g key={label}><path d={`M${p[0]},${p[1]}h-24`} stroke={C.gold} strokeWidth='1.5'/><text x={p[0]-33} y={p[1]+8} textAnchor='end' fill={C.gold} fontSize='25' fontFamily='Geist'>{label}</text></g>})}</svg>}
 if(shot===3){const a=thetaAt(t)*Math.PI/180,proj=(p:number[])=>projectPoint(p,[8,8,10],[.05,-.7,1.4],127,[2,-.8,0]);const normal=proj([0,0,5.15]),angle=proj([1.45*Math.sin(a/2),0,1.45*Math.cos(a/2)]);return <svg width='1920' height='1080' style={{position:'absolute',inset:0,pointerEvents:'none'}}><text x={normal[0]-18} y={normal[1]+18} textAnchor='end' fill={C.muted} fontSize='19'>Panel normal · 0°</text>{a>.08&&<text x={angle[0]-15} y={angle[1]+28} textAnchor='end' fill={C.gold} fontSize='23'>{thetaAt(t).toFixed(0)}°</text>}</svg>}
 return null;
}

const descriptions=[
 ['Planar aperture','A panel fixed to the spacecraft.'],
 ['One aperture','Repeated elements create a steerable beam.'],
 ['Aperture → feed → backing','Simplified layers expose the mechanism.'],
 ['Main lobe + sidelobes','Normalized ideal array factor.'],
 ['Changing geometry','Pointing changes while the panel stays fixed.'],
 ['Phase → interference → pointing','Small changes at the elements. A new direction.']
];
export function Film(){const frame=useCurrentFrame(),shot=shotAt(frame),t=(frame-shot*360)/60;const enter=ramp(t,0,.65);const isFirst=shot===0;return <AbsoluteFill style={{backgroundColor:C.paper,color:C.green,fontFamily:'Geist, sans-serif'}}>
 <style>{`@font-face{font-family:Geist;src:url(${staticFile('Geist-Regular.woff2')});font-weight:400}@font-face{font-family:Geist;src:url(${staticFile('Geist-Medium.woff2')});font-weight:500}@font-face{font-family:Geist;src:url(${staticFile('Geist-SemiBold.woff2')});font-weight:600}`}</style>
 <Img src={staticFile('paper.png')} style={{position:'absolute',inset:0,width:'100%',height:'100%',opacity:.36}}/>
 <Scene shot={shot} t={t}/><GeometryLabels shot={shot} t={t}/>
 <div style={{position:'absolute',left:120,top:75,fontSize:21,fontWeight:500,letterSpacing:2,color:C.gold}}>{chapters[shot]}</div>
 <div style={{position:'absolute',left:118,top:137,transform:`translateY(${(1-enter)*13}px)`,opacity:enter}}>
 <div style={{fontSize:isFirst?76:66,fontWeight:500,lineHeight:1.12,letterSpacing:-2.7}}>{titles[shot][0]}</div>
 <div style={{marginTop:20,fontSize:29,color:C.muted}}>{titles[shot][1]}</div>
 </div>
 {shot===3&&<PhaseData t={t}/>}
 {shot===2&&<div style={{position:'absolute',left:124,top:423,width:340,opacity:ramp(t,.6,1.6)}}>{[['01','Radiating patches'],['02','Phase-controlled feed'],['03','Structural backing']].map(([n,label],i)=><div key={n} style={{marginBottom:63,opacity:ramp(t,.6+i*.32,1.4+i*.32)}}><span style={{fontSize:20,color:C.gold}}>{n}</span><div style={{fontSize:29,marginTop:12}}>{label}</div></div>)}</div>}
 {shot!==3&&shot!==2&&<div style={{position:'absolute',left:124,top:400,width:340,opacity:ramp(t,.6,1.5)}}>
 <div style={{width:60,height:2,background:C.gold,marginBottom:24}}/>
 <div style={{fontSize:29,lineHeight:1.4,fontWeight:500}}>{descriptions[shot][0]}</div>
 <div style={{fontSize:23,lineHeight:1.6,marginTop:15,color:C.muted}}>{descriptions[shot][1]}</div>
 {shot===4&&<div style={{fontSize:58,marginTop:42,fontWeight:500,letterSpacing:-2,color:C.gold}}>{pointingState(t).theta.toFixed(0)}°<div style={{fontSize:19,letterSpacing:0,marginTop:7,color:C.muted}}>illustrative look angle</div></div>}
 </div>}
 {shot===3&&<div style={{position:'absolute',right:126,bottom:137,textAlign:'right'}}><div style={{fontSize:23,fontWeight:500}}>Main lobe + sidelobes</div><div style={{fontSize:19,color:C.muted,marginTop:8}}>Normalized ideal array factor</div></div>}
 <div style={{position:'absolute',left:120,right:120,bottom:63,display:'flex',justifyContent:'space-between',alignItems:'center',fontSize:20}}><span>LeoGuoLabs</span><div style={{display:'flex',alignItems:'center',gap:12}}>{Array.from({length:6},(_,i)=><div key={i} style={{width:i===shot?64:24,height:2,background:i<=shot?C.gold:'#d2d7c9'}}/>)}</div><span style={{fontSize:18,color:C.muted}}>SATELLITE SYSTEMS</span></div>
 <Audio src={staticFile('soundtrack.wav')}/>
 </AbsoluteFill>}
