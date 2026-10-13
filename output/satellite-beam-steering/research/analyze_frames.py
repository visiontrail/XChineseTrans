#!/usr/bin/env python3
"""Decode every reference frame; measure changes without claiming semantic optical flow.
Frame indices are zero-based. Pixel metrics use a 480-pixel-wide decoded copy.
"""
from pathlib import Path
from fractions import Fraction
import argparse, csv, json, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

p=argparse.ArgumentParser(); p.add_argument('video'); p.add_argument('--out',required=True); p.add_argument('--prefix',default='reference'); p.add_argument('--contact',action='append',default=[],help='name:comma-separated zero-based frame numbers'); a=p.parse_args()
video=Path(a.video).resolve(); out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)])); (out/f'{a.prefix}-ffprobe.json').write_text(json.dumps(probe,indent=2))
v=next(s for s in probe['streams'] if s['codec_type']=='video');fps=float(Fraction(v['avg_frame_rate'])); w=480;h=round(v['height']/v['width']*w);size=w*h*3
raw=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-vf',f'scale={w}:{h}','-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
audio=None
if any(s['codec_type']=='audio' for s in probe['streams']):
    audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-ac','1','-ar','16000','-f','f32le','-']),dtype='<f4')
rows=[];prev=None;prevhist=None;i=0
while True:
    data=raw.stdout.read(size)
    if not data:break
    if len(data)!=size:raise RuntimeError(f'Truncated frame {i}: {len(data)}/{size}')
    rgb=np.frombuffer(data,dtype=np.uint8).reshape((h,w,3)).astype(np.float32)
    y=rgb@np.array([.2126,.7152,.0722],np.float32)
    hist=np.histogram(y,bins=32,range=(0,256))[0]/(w*h)
    row={'frame':i,'time_s':round(i/fps,6),'mean_luma_0_255':round(float(y.mean()),5),'std_luma':round(float(y.std()),5),'edge_density_gt20':round(float((np.abs(np.diff(y,axis=1))>20).mean()),7)}
    if prev is None:mae=p95=changed=histdiff=0.;bbox=''
    else:
        delta=np.abs(rgb-prev).mean(axis=2);mask=delta>12
        mae=float(delta.mean());p95=float(np.quantile(delta,.95));changed=float(mask.mean());histdiff=float(np.abs(hist-prevhist).sum()/2)
        yy,xx=np.where(mask);bbox='' if not len(xx) else f'{int(xx.min())},{int(yy.min())},{int(xx.max())},{int(yy.max())}'
    row.update(rgb_mae_vs_prev=round(mae,6),rgb_delta_p95=round(p95,6),changed_fraction_gt12=round(changed,7),luma_hist_distance=round(histdiff,7),change_bbox_480wide=bbox)
    if audio is not None:
        seg=audio[round(i/fps*16000):round((i+1)/fps*16000)]
        rms=float(np.sqrt(np.mean(seg**2))) if len(seg) else 0.; peak=float(np.abs(seg).max()) if len(seg) else 0.
        row.update(audio_rms_dbfs=round(20*math.log10(max(rms,1e-12)),4),audio_peak_dbfs=round(20*math.log10(max(peak,1e-12)),4))
    rows.append(row);prev=rgb;prevhist=hist;i+=1
err=raw.stderr.read().decode();code=raw.wait()
if code:raise RuntimeError(err)
with (out/f'{a.prefix}-all-frames.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary={'video':str(video),'fps':fps,'width':v['width'],'height':v['height'],'decoded_frames':i,'ffprobe_nb_read_frames':v.get('nb_read_frames'),'duration_s':i/fps,'metric_resolution':[w,h],'threshold_note':'changed_fraction_gt12 counts RGB mean absolute change > 12/255; it is not optical-flow speed. Audio values are mono window RMS and sample peak, not LUFS or true peak.','largest_changes':sorted(rows,key=lambda x:x['rgb_mae_vs_prev'],reverse=True)[:30]}
(out/f'{a.prefix}-metrics-summary.json').write_text(json.dumps(summary,indent=2))
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
font=ImageFont.truetype(fontpath,18) if Path(fontpath).exists() else ImageFont.load_default()
for spec in a.contact:
    name,fs=spec.split(':',1);frames=[int(s) for s in fs.split(',')];fd=out/f'{a.prefix}-{name}-frames';fd.mkdir(exist_ok=True)
    select='+'.join(f'eq(n\\,{n})' for n in frames)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'select={select},scale=960:-1','-vsync','0',str(fd/'%03d.jpg')],check=True)
    cols=4;cw=480;ch=round(v['height']/v['width']*cw);rh=ch+35;sheet=Image.new('RGB',(cols*cw,math.ceil(len(frames)/cols)*rh),(240,240,240));d=ImageDraw.Draw(sheet)
    for j,(frame,imgpath) in enumerate(zip(frames,sorted(fd.glob('*.jpg')))):
        im=Image.open(imgpath).convert('RGB').resize((cw,ch));x=(j%cols)*cw;y=(j//cols)*rh;sheet.paste(im,(x,y));d.text((x+8,y+ch+6),f'F{frame:05d}  {frame/fps:.3f}s',font=font,fill=(15,20,20))
    sheet.save(out/f'{a.prefix}-contact-{name}.jpg',quality=92)
print(json.dumps({k:summary[k] for k in ['video','fps','width','height','decoded_frames','duration_s']},ensure_ascii=False))
