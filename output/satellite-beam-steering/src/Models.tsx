import React,{useMemo} from 'react';
import * as THREE from 'three';
export const C={paper:'#FDFBF7',green:'#1A4A3A',muted:'#426454',gold:'#80601B',metal:'#c8c7b8',foil:'#b59a55',cell:'#1d4c47',yellow:'#E5C158'};
export function Box({p=[0,0,0],s=[1,1,1],color=C.paper,metal=.1,rough=.45,...props}:any){return <mesh position={p} {...props}><boxGeometry args={s}/><meshStandardMaterial color={color} metalness={metal} roughness={rough}/></mesh>}
export function RoundBox({p=[0,0,0],s=[1,1,1],color=C.paper,bevel=.07,...props}:any){
 const geom=useMemo(()=>{const [w,h,d]=s;const a=new THREE.Shape();a.moveTo(-w/2+bevel,-h/2);a.lineTo(w/2-bevel,-h/2);a.quadraticCurveTo(w/2,-h/2,w/2,-h/2+bevel);a.lineTo(w/2,h/2-bevel);a.quadraticCurveTo(w/2,h/2,w/2-bevel,h/2);a.lineTo(-w/2+bevel,h/2);a.quadraticCurveTo(-w/2,h/2,-w/2,h/2-bevel);a.lineTo(-w/2,-h/2+bevel);a.quadraticCurveTo(-w/2,-h/2,-w/2+bevel,-h/2);const g=new THREE.ExtrudeGeometry(a,{depth:d,bevelEnabled:true,bevelThickness:bevel/2,bevelSize:bevel/2,bevelSegments:3,steps:1,curveSegments:5});g.translate(0,0,-d/2);return g;},s);
 return <mesh position={p} geometry={geom} {...props}><meshStandardMaterial color={color} roughness={.38} metalness={.32}/></mesh>
}
export function Line3D({points,color=C.green,width=.008,opacity=1}:any){
 const geo=useMemo(()=>new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points.map((p:any)=>new THREE.Vector3(...p))),Math.max(8,points.length*3),width,5,false),[JSON.stringify(points),width]);
 return <mesh geometry={geo}><meshBasicMaterial color={color} transparent={opacity<1} opacity={opacity}/></mesh>
}
export function Bolts({w=2.25,h=2.25,z=.12}:any){return <>{[-1,1].flatMap(x=>[-1,1].map(y=><mesh key={`${x}${y}`} position={[x*w/2,y*h/2,z]} rotation={[Math.PI/2,0,0]}><cylinderGeometry args={[.042,.042,.018,12]}/><meshStandardMaterial color={C.green} metalness={.6} roughness={.2}/></mesh>))}</>}
export function ArrayPanel({explode=0,phase=0}:any){
 return <group>
 <RoundBox p={[0,0,-.13]} s={[2.4,2.4,.16]} color={C.metal}/>
 {Array.from({length:11},(_,i)=><Box key={`sink${i}`} p={[-1.05+i*.21,0,-.26]} s={[.038,2.2,.24]} color={C.metal} metal={.6}/>)}
 <group position={[0,0,explode*.85]}>
 <RoundBox s={[2.28,2.28,.1]} color={C.green}/>
 {Array.from({length:8},(_,i)=><React.Fragment key={`feed${i}`}>
 <Box p={[-.91+i*.26,0,.095]} s={[.018,2,.012]} color={C.foil} metal={.7}/>
 {Array.from({length:8},(_,j)=><Box key={j} p={[-.91+i*.26,-.91+j*.26,.09]} s={[.09,.09,.04]} color={C.paper}/>)}
 </React.Fragment>)}
 </group>
 <group position={[0,0,.14+explode*1.9]}>
 <RoundBox s={[2.4,2.4,.105]} color='#dedac7'/>
 {Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>
 <group key={`${i},${j}`} position={[-.91+i*.26,-.91+j*.26,.115]}>
 <Box s={[.18,.18,.014]} color={C.foil} metal={.7} rough={.3}/>
 <Box p={[0,-.105,.002]} s={[.018,.035,.012]} color={C.gold}/>
 <Box p={[0,-.102,.013]} s={[.035,.008,.009]} color={C.paper}/>
 </group>))}
 <Bolts z={.12}/>
 </group>
 </group>
}
function SolarWing({side=1}:any){return <group position={[side*4.05,0,-.1]}>
 <Box s={[3.4,2.35,.1]} color={C.metal}/>
 {Array.from({length:12},(_,i)=>Array.from({length:8},(_,j)=><Box key={`${i}:${j}`} p={[-1.56+i*.284,-1.026+j*.293,.065]} s={[.267,.272,.015]} color={C.cell} metal={.45} rough={.28}/>))}
 {Array.from({length:12},(_,i)=><Box key={i} p={[-1.56+i*.284,0,.076]} s={[.008,2.24,.003]} color='#b0baaf' metal={.5}/>)}
 <Box p={[0,0,.08]} s={[3.35,.015,.005]} color={C.foil} metal={.7}/>
 <Box p={[0,0,-.1]} s={[3.4,.1,.12]} color={C.green}/>
 </group>}
export function Satellite({array=true}:any){return <group>
 <RoundBox s={[2.7,2.6,1.45]} color={C.paper} bevel={.14}/>
 <Box p={[0,0,-.73]} s={[2.6,2.5,.12]} color={C.foil} metal={.65} rough={.4}/>
 {[-1,1].map(side=><React.Fragment key={side}>
 <Box p={[side*1.36,0,0]} s={[.04,2.38,1.2]} color={C.metal} metal={.55}/>
 {Array.from({length:13},(_,i)=><Box key={i} p={[side*1.39,-1.04+i*.174,0]} s={[.04,.035,1.18]} color={C.paper}/>)}
 <Box p={[side*2.01,0,-.1]} s={[1.3,.14,.16]} color={C.green} metal={.5}/>
 <mesh position={[side*1.75,0,-.1]} rotation={[0,0,Math.PI/2]}><cylinderGeometry args={[.18,.18,.35,24]}/><meshStandardMaterial color={C.metal} metalness={.5} roughness={.3}/></mesh>
 <SolarWing side={side}/>
 <Box p={[side*1.1,1.34,.12]} s={[.25,.12,1.05]} color={C.foil} metal={.6}/>
 <mesh position={[side*.94,1.5,-.35]}><cylinderGeometry args={[.10,.14,.2,24]}/><meshStandardMaterial color={C.green}/></mesh>
 </React.Fragment>)}
 {array&&<group position={[0,0,.86]} scale={.91}><ArrayPanel/></group>}
 <Line3D points={[[.9,1.3,0],[1.1,1.9,.1],[.6,2.1,.15]]} color={C.green} width={.025}/>
 <mesh position={[.6,2.1,.15]}><sphereGeometry args={[.065,16,16]}/><meshStandardMaterial color={C.gold}/></mesh>
 </group>}
export function Beam({from,to,r=.6,opacity=.12}:any){
 const p=new THREE.Vector3(...from),q=new THREE.Vector3(...to),v=q.clone().sub(p),mid=p.clone().add(q).multiplyScalar(.5);const quat=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),v.clone().normalize());
 const cone=useMemo(()=>{const g=new THREE.ConeGeometry(r,v.length(),48,1,true);g.rotateZ(Math.PI);return g},[r,v.length()]);
 return <group><mesh geometry={cone} position={mid} quaternion={quat}><meshBasicMaterial color={C.green} side={THREE.DoubleSide} transparent opacity={opacity} depthWrite={false}/></mesh><Line3D points={[from,to]} color={C.gold} width={.015}/></group>
}
export function Globe({radius=9,position=[0,-11,0]}:any){
 const lat=useMemo(()=>Array.from({length:7},(_,i)=>{const phi=(i-3)*.15;return Array.from({length:73},(_,j)=>{const t=(j/72)*Math.PI*2;return [radius*Math.cos(phi)*Math.sin(t),radius*Math.sin(phi),radius*Math.cos(phi)*Math.cos(t)]})}),[radius]);
 return <group position={position} rotation={[.4,0,.25]}>
 <mesh><sphereGeometry args={[radius,96,64]}/><meshStandardMaterial color='#e7eadd' roughness={.9}/></mesh>
 {lat.map((points,i)=><Line3D key={i} points={points.map(p=>p.map(x=>x*1.0003))} color='#9bab9b' width={.009}/>)}
 {Array.from({length:15},(_,i)=><Line3D key={i} points={Array.from({length:73},(_,j)=>{const a=j/72*Math.PI*2,b=i/15*Math.PI;return [radius*1.0003*Math.sin(a)*Math.cos(b),radius*1.0003*Math.cos(a),radius*1.0003*Math.sin(a)*Math.sin(b)]})} color='#9bab9b' width={.009}/>)}
 </group>
}
