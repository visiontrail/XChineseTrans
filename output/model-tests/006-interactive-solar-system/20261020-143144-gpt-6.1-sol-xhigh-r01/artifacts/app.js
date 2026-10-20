'use strict';

// Circular illustrative orbits; one shared clock preserves relative orbital periods.
const PLANETS = [
  {id:'mercury',name:'Mercury',category:'TERRESTRIAL PLANET',color:'#a69b8c',orbit:64,radius:4.8,period:87.97,phase:2.5,diameter:'4,879',distance:'0.39',year:['88','days'],day:['58.6','days'],tagline:'Small world. Extreme conditions.',description:'The smallest planet lives closest to the Sun. Its cratered surface swings between scorching days and bitterly cold nights.',fact:'Despite being closest to the Sun, Mercury is not the hottest planet.',texture:'rock',seed:12},
  {id:'venus',name:'Venus',category:'TERRESTRIAL PLANET',color:'#d8bd86',orbit:99,radius:8,period:224.7,phase:4.8,diameter:'12,104',distance:'0.72',year:['225','days'],day:['243','days'],tagline:'Beautiful from a distance.',description:'A thick blanket of carbon dioxide traps heat beneath pale clouds. Venus is our nearest planetary neighbor in size, but a very different world.',fact:'Venus rotates so slowly that one rotation lasts longer than its year.',texture:'cloud',seed:27},
  {id:'earth',name:'Earth',category:'TERRESTRIAL PLANET',color:'#6398b8',orbit:139,radius:9.4,period:365.25,phase:5.95,diameter:'12,742',distance:'1.00',year:['365.25','days'],day:['23.9','hours'],tagline:'A world like no other.',description:'Our pale blue dot is the only world known to support life, wrapped in an atmosphere that keeps liquid water on its surface.',fact:'Sunlight takes about 8 minutes and 20 seconds to reach Earth.',texture:'earth',seed:34},
  {id:'mars',name:'Mars',category:'TERRESTRIAL PLANET',color:'#c46b46',orbit:181,radius:6.6,period:686.98,phase:2.1,diameter:'6,779',distance:'1.52',year:['1.88','Earth years'],day:['24.6','hours'],tagline:'The next great horizon.',description:'Rust-colored deserts, polar ice, and ancient riverbeds hint at a wetter past. Mars is a rocky world with a familiar rhythm of days and seasons.',fact:'Olympus Mons on Mars is the tallest known volcano in the solar system.',texture:'rock',seed:43},
  {id:'jupiter',name:'Jupiter',category:'GAS GIANT',color:'#c2a17f',orbit:269,radius:28,period:4332.59,phase:3.85,diameter:'139,820',distance:'5.20',year:['11.86','Earth years'],day:['9.9','hours'],tagline:'A world of superlatives.',description:'The largest planet is a swirling ocean of gas. Bright cloud bands and enormous storms race around a world with no solid surface to stand on.',fact:'Jupiter has more than twice the mass of all the other planets combined.',texture:'jupiter',seed:54},
  {id:'saturn',name:'Saturn',category:'GAS GIANT',color:'#cbb68b',orbit:343,radius:23,period:10759.22,phase:0.50,diameter:'116,460',distance:'9.58',year:['29.46','Earth years'],day:['10.7','hours'],tagline:'The solar system’s showstopper.',description:'A delicate-looking ring system surrounds this gas giant. The rings are made of countless pieces of ice and rock, from tiny grains to large chunks.',fact:'Saturn’s average density is lower than that of water.',texture:'saturn',seed:65},
  {id:'uranus',name:'Uranus',category:'ICE GIANT',color:'#8ec5cb',orbit:420,radius:15.6,period:30688.5,phase:2.8,diameter:'50,724',distance:'19.2',year:['84.02','Earth years'],day:['17.2','hours'],tagline:'A different way to go around.',description:'Pale blue-green clouds hide a cold, deep atmosphere. Uranus is tipped so far over that it rolls around the Sun on its side.',fact:'Uranus’s rotation axis is tilted by about 98 degrees.',texture:'ice',seed:76},
  {id:'neptune',name:'Neptune',category:'ICE GIANT',color:'#4a77c8',orbit:495,radius:15.1,period:60182,phase:5.43,diameter:'49,244',distance:'30.1',year:['164.8','Earth years'],day:['16.1','hours'],tagline:'At the edge of the planetary realm.',description:'Dark, cold, and swept by powerful winds, Neptune circles the Sun far beyond Earth. Methane in its atmosphere helps give it its blue appearance.',fact:'Neptune was predicted with mathematics before it was seen through a telescope.',texture:'neptune',seed:87}
];
const SUN={id:'sun',name:'Sun',category:'OUR STAR',color:'#efb064',radius:34,diameter:'1,392,700',distance:'—',year:['—',''],day:['~27','Earth days'],tagline:'Everything revolves around it.',description:'A star at the center of our neighborhood. Nuclear fusion in its core supplies the light and heat that make life on Earth possible.',fact:'The Sun holds about 99.8% of the mass of the solar system.',texture:'sun',seed:9};
const $=id=>document.getElementById(id);
const canvas=$('space');
const ctx=canvas.getContext('2d');
const TAU=Math.PI*2;
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
const initial={angle:-0.14,tilt:0.49};
const state={selected:PLANETS[2],days:0,paused:reducedMotion.matches,speed:20,zoom:1,angle:initial.angle,tilt:initial.tilt,view:'perspective',labels:true,orbits:true,hover:null};
let width=0,height=0,dpr=1,layout=null,points=[],lastFrame=0,lastUI=-1,portraitFrame=0;
const pointers=new Map();
let gesture=null;

function rng(seed){return()=>{seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function clamp(v,min,max){return Math.min(max,Math.max(min,v))}
function mix(a,b,t){return a+(b-a)*t}
function hex(hex){return hex.match(/[\da-f]{2}/gi).map(x=>parseInt(x,16))}

// Deterministic procedural surfaces keep the atlas self-contained and offline-ready.
function makeTexture(body){
  const w=512,h=256,c=document.createElement('canvas');c.width=w;c.height=h;
  const cctx=c.getContext('2d'),random=rng(body.seed),base=hex(body.color);
  cctx.fillStyle=body.color;cctx.fillRect(0,0,w,h);
  if(body.texture==='earth'){
    cctx.fillStyle='#245a81';cctx.fillRect(0,0,w,h);
    const lands=[[[.07,.28],[.14,.18],[.23,.16],[.28,.25],[.25,.34],[.20,.36],[.20,.44],[.14,.42],[.09,.35]],[[.23,.44],[.29,.47],[.32,.58],[.29,.68],[.26,.83],[.23,.71],[.23,.59],[.20,.49]],[[.45,.30],[.50,.23],[.58,.24],[.65,.17],[.76,.20],[.85,.27],[.89,.35],[.79,.43],[.72,.39],[.68,.47],[.61,.43],[.56,.35]],[[.46,.38],[.54,.38],[.59,.47],[.56,.62],[.51,.71],[.47,.59],[.43,.48]],[[.78,.64],[.86,.61],[.91,.69],[.87,.78],[.80,.75]],[[.32,.1],[.39,.12],[.37,.22],[.33,.24]]];
    for(const poly of lands){cctx.beginPath();poly.forEach((p,i)=>i?cctx.lineTo(p[0]*w,p[1]*h):cctx.moveTo(p[0]*w,p[1]*h));cctx.closePath();cctx.fillStyle='#758e6b';cctx.fill();}
    cctx.fillStyle='#d1d7cc';cctx.fillRect(0,0,w,12);cctx.fillRect(0,h-15,w,15);
    for(let i=0;i<130;i++){cctx.fillStyle=`rgba(238,243,231,${random()*.48})`;cctx.beginPath();cctx.ellipse(random()*w,random()*h,4+random()*32,1+random()*5,-.2,0,TAU);cctx.fill();}
  } else if(['jupiter','saturn','cloud','neptune','ice'].includes(body.texture)){
    for(let y=0;y<h;y++){
      const band=Math.sin(y*.21+Math.sin(y*.051)*3)*.15+Math.sin(y*.73)*.07+(random()-.5)*.045;
      cctx.fillStyle=`rgb(${base.map(v=>clamp(Math.round(v*(1+band)),0,255)).join(',')})`;
      cctx.fillRect(0,y,w,1);
    }
    for(let i=0;i<130;i++){
      const y=random()*h,alpha=random()*(body.texture==='ice'?.035:.12);
      cctx.fillStyle=`rgba(255,246,222,${alpha})`;cctx.beginPath();cctx.ellipse(random()*w,y,8+random()*70,1+random()*5,0,0,TAU);cctx.fill();
    }
    if(body.texture==='jupiter'){
      cctx.fillStyle='#a86e50';cctx.beginPath();cctx.ellipse(w*.69,h*.64,28,10,-.05,0,TAU);cctx.fill();
      cctx.strokeStyle='#e0c0a0';cctx.lineWidth=3;cctx.stroke();
    }
  } else {
    for(let i=0;i<1800;i++){
      const x=random()*w,y=random()*h,r=.5+random()*5;
      cctx.fillStyle=`rgba(${random()>.5?'255,241,214':'35,24,21'},${random()*.17})`;
      cctx.beginPath();cctx.ellipse(x,y,r*1.4,r,0,0,TAU);cctx.fill();
    }
    if(body.id==='mars'){cctx.fillStyle='#e7d3b5';cctx.fillRect(0,0,w,9);cctx.fillRect(0,h-5,w,5);}
  }
  return cctx.getImageData(0,0,w,h);
}

const textureCache=new Map();
const spriteCache=new Map();
for(const body of [...PLANETS,SUN])textureCache.set(body.id,makeTexture(body));

function sphere(body,lightAngle=-.7,rotation=0){
  const bucket=Math.round(lightAngle*12),rot=Math.round(rotation*12);
  const key=`${body.id}:${bucket}:${rot}`;
  if(spriteCache.has(key))return spriteCache.get(key);
  const size=128,s=size/2-2,texture=textureCache.get(body.id);
  const c=document.createElement('canvas');c.width=size;c.height=size;
  const cc=c.getContext('2d'),pixels=cc.createImageData(size,size),rgb=pixels.data;
  const lx=Math.cos(bucket/12)*.79,ly=Math.sin(bucket/12)*.79,lz=.61;
  for(let y=0;y<size;y++)for(let x=0;x<size;x++){
    const nx=(x-size/2)/s,ny=(y-size/2)/s,r2=nx*nx+ny*ny;
    if(r2>1)continue;
    const nz=Math.sqrt(1-r2),u=((Math.atan2(nx,nz)/TAU+.5+rot/12/TAU)%1+1)%1,v=Math.acos(-ny)/Math.PI;
    const ti=(Math.min(255,Math.floor(v*256))*512+Math.min(511,Math.floor(u*512)))*4;
    const lambert=Math.max(0,nx*lx+ny*ly+nz*lz);
    let shade=body.id==='sun'?.79+nz*.28:.10+.90*lambert;
    const rim=Math.pow(1-nz,4)*(body.id==='earth'?.24:body.id==='neptune'?.1:0);
    const i=(y*size+x)*4;
    rgb[i]=texture.data[ti]*shade+rim*60;
    rgb[i+1]=texture.data[ti+1]*shade+rim*150;
    rgb[i+2]=texture.data[ti+2]*shade+rim*200;
    rgb[i+3]=clamp((1-Math.sqrt(r2))*s*255,0,255);
  }
  cc.putImageData(pixels,0,0);
  if(spriteCache.size>160)spriteCache.delete(spriteCache.keys().next().value);
  spriteCache.set(key,c);return c;
}

function rings(c,x,y,r,front){
  c.save();c.translate(x,y);c.rotate(-.32);c.scale(1,.34);
  const start=front?0:Math.PI,end=front?Math.PI:TAU;
  for(let i=0;i<18;i++){
    const rr=r*(1.3+i*.044);
    c.beginPath();c.arc(0,0,rr,start,end);c.lineWidth=r*.038;
    c.strokeStyle=i===10?'rgba(20,22,26,.75)':`rgba(206,190,153,${.38+Math.sin(i*2.3)*.17})`;c.stroke();
  }c.restore();
}

function drawBody(c,body,x,y,r,light=-.7,rotation=0){
  if(body.id==='sun'){
    const glow=c.createRadialGradient(x,y,r*.4,x,y,r*4.7);
    glow.addColorStop(0,'rgba(244,165,75,.20)');glow.addColorStop(.35,'rgba(227,136,49,.075)');glow.addColorStop(1,'rgba(227,136,49,0)');
    c.fillStyle=glow;c.fillRect(x-r*4.7,y-r*4.7,r*9.4,r*9.4);
    c.save();c.shadowColor='#eda856';c.shadowBlur=r*.45;c.fillStyle='#d39040';c.beginPath();c.arc(x,y,r*.95,0,TAU);c.fill();c.restore();
  }
  if(body.id==='saturn')rings(c,x,y,r,false);
  c.drawImage(sphere(body,light,rotation),x-r,y-r,r*2,r*2);
  if(body.id==='saturn')rings(c,x,y,r,true);
}

const random=rng(4096);
const stars=Array.from({length:420},()=>({x:random(),y:random(),r:random()>.96?1.05:.25+random()*.5,a:.1+random()*.5}));
const asteroids=Array.from({length:700},()=>({angle:random()*TAU,r:211+random()*25,size:.25+random()*.55,a:.08+random()*.20}));

function resize(){
  const rect=canvas.getBoundingClientRect();width=rect.width;height=rect.height;dpr=Math.min(devicePixelRatio||1,2);
  canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);
  const compact=width<=850;
  const panelWidth=width>1600?410:width>1150?360:305;
  const available=compact?width:width-panelWidth;
  const mobile=width<=520;
  const top=compact?(mobile?180:145):140;
  const sceneHeight=compact?(mobile?277:320):height-top-65;
  const baseScale=compact?Math.min((width-38)/1030,sceneHeight/(1030*.49)):Math.min((available-70)/1030,(height-140)/(1030*.49));
  layout={cx:compact?width*.5:available*.51+14,cy:compact?top+sceneHeight*.5:height*.55+12,scale:baseScale,compact,mobile};
}
new ResizeObserver(resize).observe(canvas);

function project(radius,angle){
  const a=angle+state.angle,s=layout.scale*state.zoom;
  return{x:layout.cx+Math.cos(a)*radius*s,y:layout.cy+Math.sin(a)*radius*s*state.tilt,depth:Math.sin(a)};
}
function pathOrbit(radius){
  ctx.beginPath();ctx.ellipse(layout.cx,layout.cy,radius*layout.scale*state.zoom,radius*layout.scale*state.zoom*state.tilt,0,0,TAU);
}
function render(now){
  requestAnimationFrame(render);
  if(!layout||document.hidden){lastFrame=now;return;}
  const dt=Math.min((now-(lastFrame||now))/1000,.1);lastFrame=now;
  if(!state.paused)state.days+=dt*state.speed;
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);
  const atmosphere=ctx.createRadialGradient(layout.cx,layout.cy,0,layout.cx,layout.cy,width*.5);
  atmosphere.addColorStop(0,'#14151a');atmosphere.addColorStop(.4,'#0e1117');atmosphere.addColorStop(1,'#090c10');
  ctx.fillStyle=atmosphere;ctx.fillRect(0,0,width,height);
  for(const star of stars){
    const x=((star.x*width+state.angle*14)%width+width)%width,y=star.y*height;
    ctx.fillStyle=`rgba(195,210,228,${star.a})`;ctx.beginPath();ctx.arc(x,y,star.r,0,TAU);ctx.fill();
  }
  // Quiet reference marks around the center lend a navigational feel.
  ctx.strokeStyle='rgba(163,181,200,.055)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(layout.cx-10,layout.cy);ctx.lineTo(layout.cx+10,layout.cy);ctx.moveTo(layout.cx,layout.cy-10);ctx.lineTo(layout.cx,layout.cy+10);ctx.stroke();
  if(state.orbits){
    PLANETS.forEach(p=>{pathOrbit(p.orbit);ctx.strokeStyle=p.id===state.selected.id?'rgba(230,185,128,.30)':'rgba(167,183,207,.12)';ctx.lineWidth=p.id===state.selected.id?1:.7;ctx.stroke();});
    for(const a of asteroids){const p=project(a.r,a.angle+state.days*.00017);ctx.fillStyle=`rgba(180,170,148,${a.a})`;ctx.fillRect(p.x,p.y,a.size,a.size);}
    if(!layout.compact&&state.zoom<=1.4){const belt=project(224,2.75);ctx.fillStyle='#6a706e';ctx.font='7px "Avenir Next",sans-serif';ctx.textAlign='center';ctx.fillText('A S T E R O I D  B E L T',belt.x,belt.y-13);}
  }
  const sizes=layout.compact?Math.max(.68,layout.scale*1.55):Math.max(.7,layout.scale);
  const bodyScale=sizes*Math.pow(state.zoom,.38);
  points=PLANETS.map(p=>{
    const angle=p.phase+state.days/p.period*TAU,position=project(p.orbit,angle);
    return{...position,body:p,r:p.radius*bodyScale,light:Math.atan2((layout.cy-position.y)*.75,layout.cx-position.x)};
  });
  const sunPoint={x:layout.cx,y:layout.cy,depth:0,body:SUN,r:SUN.radius*bodyScale,light:0};
  const all=[...points,sunPoint].sort((a,b)=>a.depth-b.depth);
  for(const point of all){
    const {x,y,r,body}=point;
    if(body.id===state.selected.id){
      ctx.beginPath();ctx.arc(x,y,r+7,0,TAU);ctx.strokeStyle='rgba(230,185,128,.65)';ctx.lineWidth=.8;ctx.stroke();
      ctx.beginPath();ctx.arc(x,y,r+12,0,TAU);ctx.strokeStyle='rgba(230,185,128,.10)';ctx.stroke();
    }
    if(body.id===state.hover){ctx.beginPath();ctx.arc(x,y,r+5,0,TAU);ctx.strokeStyle='rgba(235,237,234,.6)';ctx.lineWidth=.8;ctx.stroke();}
    drawBody(ctx,body,x,y,r,point.light,0);
  }
  // Label collisions are resolved in screen space; the mobile scene prioritizes the selection.
  const placed=[],headingBounds={x:0,y:0,w:layout.compact?width:440,h:layout.compact?170:165};
  if(state.labels){
    const labels=[...all].sort((a,b)=>(b.body.id===state.selected.id)-(a.body.id===state.selected.id));
    for(const point of labels){
      const {x,y,r,body}=point,selected=body.id===state.selected.id;
      const name=body.name.toUpperCase(),fontSize=layout.mobile?7:layout.compact?8:8;
      ctx.font=`${selected?'500':'400'} ${fontSize}px "Avenir Next",sans-serif`;
      const tw=ctx.measureText(name).width+12;
      let ly=y+r+(body.id==='saturn'?15:14),lx=x;
      const box={x:lx-tw/2,y:ly-9,w:tw,h:13};
      if(x<20||x>width-20||ly<headingBounds.h&&box.x<headingBounds.w||ly>height-(layout.compact?(layout.mobile?320:275):55))continue;
      if(!selected&&placed.some(a=>box.x<a.x+a.w+3&&box.x+box.w>a.x-3&&box.y<a.y+a.h+3&&box.y+box.h>a.y-3))continue;
      ctx.fillStyle=selected?'#e6b980':body.id==='sun'?'#b39873':'#a1aab6';ctx.textAlign='center';
      ctx.fillText(name,lx,ly);placed.push(box);
      if(selected){ctx.fillStyle='#e6b980';ctx.beginPath();ctx.arc(lx-tw/2+1,ly-2.5,1.5,0,TAU);ctx.fill();}
    }
  }
  points=all;
  if(Math.floor(state.days)!==lastUI){lastUI=Math.floor(state.days);updateElapsed();}
  if(now-portraitFrame>100){portraitFrame=now;drawPortrait();}
}

function drawPortrait(){
  const c=$('planet-portrait'),pctx=c.getContext('2d');pctx.clearRect(0,0,160,160);
  drawBody(pctx,state.selected,80,80,state.selected.id==='saturn'?34:state.selected.id==='sun'?39:49,-.65,0);
}
function updateElapsed(){
  const years=Math.floor(state.days/365.25),days=Math.floor(state.days%365.25);
  $('elapsed').innerHTML=`YEAR ${String(years).padStart(2,'0')} <span>·</span> DAY ${String(days).padStart(3,'0')}`;
}
function metric(id,value,unit){$(id).replaceChildren(document.createTextNode(value+' '));const small=document.createElement('small');small.textContent=unit;$(id).append(small);}
function select(body,announce=true){
  state.selected=body;
  const index=PLANETS.indexOf(body);
  $('planet-order').textContent=index<0?'THE CENTER':`${String(index+1).padStart(2,'0')} / 08`;
  $('planet-category').textContent=body.category;
  $('planet-name').textContent=body.name;
  $('planet-tagline').textContent=body.tagline;
  $('planet-description').textContent=body.description;
  metric('stat-diameter',body.diameter,'km');metric('stat-distance',body.distance,body.id==='sun'?'':'AU');
  metric('stat-year',...body.year);metric('stat-day',...body.day);
  $('planet-fact').textContent=body.fact;
  const next=PLANETS[(index+1)%PLANETS.length];$('next-name').textContent=next.name;
  for(const button of $('planet-list').children)button.setAttribute('aria-pressed',String(button.dataset.planet===body.id));
  if(announce)$('announcement').textContent=`${body.name} selected. ${body.tagline}`;
  drawPortrait();
}

for(const [i,planet] of PLANETS.entries()){
  const button=document.createElement('button');button.className='planet-option';button.dataset.planet=planet.id;button.setAttribute('aria-label',`Explore ${planet.name}`);button.setAttribute('aria-pressed',String(i===2));
  const number=document.createElement('span');number.className='planet-number';number.textContent=String(i+1).padStart(2,'0');
  const icon=document.createElement('canvas');icon.width=144;icon.height=96;icon.setAttribute('aria-hidden','true');
  drawBody(icon.getContext('2d'),planet,72,48,planet.id==='saturn'?19:planet.id==='jupiter'?30:planet.id==='uranus'||planet.id==='neptune'?23:planet.id==='mercury'?15:planet.id==='mars'?17:23,-.65);
  const label=document.createElement('span');label.className='planet-option-name';label.textContent=planet.name;
  button.append(number,icon,label);button.addEventListener('click',()=>select(planet));$('planet-list').append(button);
}

function updatePause(){
  $('play-pause').classList.toggle('paused',state.paused);$('play-pause').setAttribute('aria-label',state.paused?'Resume simulation':'Pause simulation');$('play-pause').setAttribute('aria-pressed',String(state.paused));$('playback-label').textContent=state.paused?'TAKING A BREATHER':'IN MOTION';
}
function togglePause(){state.paused=!state.paused;updatePause();}
function zoomBy(amount){state.zoom=clamp(state.zoom+amount,.55,2.5);$('zoom-value').textContent=`${Math.round(state.zoom*100)}%`;$('zoom-in').disabled=state.zoom>=2.5;$('zoom-out').disabled=state.zoom<=.55;}
function setView(view){state.view=view;state.tilt=view==='top'?.94:initial.tilt;state.angle=initial.angle;$('perspective-view').setAttribute('aria-pressed',String(view==='perspective'));$('top-view').setAttribute('aria-pressed',String(view==='top'));}
function updateSpeed(){const val=Number($('speed').value);state.speed=[1,5,20,60,180][val];$('speed-output').textContent=`${state.speed} ${state.speed===1?'day':'days'} / sec`;$('speed').style.background=`linear-gradient(to right,var(--accent) ${val*25}%,#30353c ${val*25}%)`;$('speed').setAttribute('aria-valuetext',`${state.speed} ${state.speed===1?'day':'days'} per second`);}
function toggleFeature(feature,button){state[feature]=!state[feature];$(button).setAttribute('aria-pressed',String(state[feature]));$(button).classList.toggle('active',state[feature]);}
function reset(){state.days=0;state.angle=initial.angle;state.paused=reducedMotion.matches;state.zoom=1;setView('perspective');state.labels=true;state.orbits=true;for(const id of ['labels-toggle','orbits-toggle']){$(id).classList.add('active');$(id).setAttribute('aria-pressed','true');}$('speed').value='2';updateSpeed();updatePause();zoomBy(0);select(PLANETS[2]);updateElapsed();$('announcement').textContent='Simulation reset. Earth selected.';}

$('play-pause').addEventListener('click',togglePause);
$('speed').addEventListener('input',updateSpeed);
$('zoom-in').addEventListener('click',()=>zoomBy(.15));$('zoom-out').addEventListener('click',()=>zoomBy(-.15));
$('reset').addEventListener('click',reset);
$('perspective-view').addEventListener('click',()=>setView('perspective'));$('top-view').addEventListener('click',()=>setView('top'));
$('labels-toggle').addEventListener('click',()=>toggleFeature('labels','labels-toggle'));$('orbits-toggle').addEventListener('click',()=>toggleFeature('orbits','orbits-toggle'));
$('next-planet').addEventListener('click',()=>select(PLANETS[(PLANETS.indexOf(state.selected)+1)%8]));

function bodyAt(x,y){return [...points].reverse().find(p=>Math.hypot(x-p.x,y-p.y)<Math.max(p.r+(p.body.id==='saturn'?12:7),18));}
function pointerPosition(e){const r=canvas.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
function touchDistance(){const p=[...pointers.values()];return p.length>=2?Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y):0;}
canvas.addEventListener('pointerdown',e=>{
  if(e.button!==0)return;
  const p=pointerPosition(e);pointers.set(e.pointerId,p);canvas.setPointerCapture(e.pointerId);
  gesture={start:p,previous:p,moved:false,dist:touchDistance(),startZoom:state.zoom,multi:pointers.size>1};canvas.classList.add('dragging');$('planet-tooltip').hidden=true;
});
canvas.addEventListener('pointermove',e=>{
  const p=pointerPosition(e);
  if(pointers.has(e.pointerId)&&gesture){
    pointers.set(e.pointerId,p);
    if(pointers.size>=2){
      gesture.multi=true;gesture.moved=true;const distance=touchDistance();
      if(gesture.dist>0){state.zoom=clamp(gesture.startZoom*distance/gesture.dist,.55,2.5);zoomBy(0);}else{gesture.dist=distance;gesture.startZoom=state.zoom;}
    } else {
      if(Math.hypot(p.x-gesture.start.x,p.y-gesture.start.y)>5)gesture.moved=true;
      if(gesture.moved){state.angle+=(p.x-gesture.previous.x)*.006;state.tilt=clamp(state.tilt+(p.y-gesture.previous.y)*.0025,.23,.98);}
    }
    gesture.previous=p;return;
  }
  const hit=bodyAt(p.x,p.y);state.hover=hit?hit.body.id:null;
  canvas.style.cursor=hit?'pointer':'grab';
  const tooltip=$('planet-tooltip');tooltip.hidden=!hit;
  if(hit){tooltip.textContent=`${hit.body.name} ↗`;tooltip.style.left=`${clamp(p.x+15,10,width-100)}px`;tooltip.style.top=`${clamp(p.y-35,10,height-40)}px`;}
});
function endPointer(e){
  const p=pointerPosition(e);
  if(gesture&&!gesture.moved&&!gesture.multi){const hit=bodyAt(p.x,p.y);if(hit)select(hit.body);}
  pointers.delete(e.pointerId);
  if(!pointers.size){gesture=null;canvas.classList.remove('dragging');}
  else if(gesture){gesture.previous=[...pointers.values()][0];gesture.start=gesture.previous;gesture.moved=true;}
}
canvas.addEventListener('pointerup',endPointer);canvas.addEventListener('pointercancel',e=>{pointers.delete(e.pointerId);gesture=null;canvas.classList.remove('dragging');});
canvas.addEventListener('pointerleave',()=>{state.hover=null;$('planet-tooltip').hidden=true;});
canvas.addEventListener('wheel',e=>{e.preventDefault();zoomBy(e.deltaY>0?-.07:.07);},{passive:false});

for(const [button,id] of [['about-button','about-dialog'],['scale-info','about-dialog'],['help-button','help-dialog']])$(button).addEventListener('click',()=>$(id).showModal());
for(const dialog of document.querySelectorAll('dialog')){
  dialog.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
}
document.addEventListener('keydown',e=>{
  if(document.querySelector('dialog[open]')||e.target.matches('input,textarea,select')||e.altKey||e.ctrlKey||e.metaKey)return;
  if(e.code==='Space'&&!e.target.closest('button,a')){e.preventDefault();togglePause();}
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
    e.preventDefault();const direction=e.key==='ArrowRight'?1:-1;const i=PLANETS.indexOf(state.selected);select(PLANETS[(i+direction+8)%8]);
  }
  if(e.key==='+'||e.key==='='){e.preventDefault();zoomBy(.15);}if(e.key==='-'||e.key==='_'){e.preventDefault();zoomBy(-.15);}if(e.key.toLowerCase()==='r')reset();
});
reducedMotion.addEventListener('change',e=>{if(e.matches){state.paused=true;updatePause();}});
document.addEventListener('visibilitychange',()=>{lastFrame=0;});
select(PLANETS[2],false);updatePause();updateSpeed();updateElapsed();resize();requestAnimationFrame(render);
