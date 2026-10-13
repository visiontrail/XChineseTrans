#!/usr/bin/env python3
"""Deterministic original stereo score. Event IDs are shared with the visual timeline."""
import json, wave, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
root=Path(__file__).resolve().parent.parent
cfg=json.loads((root/'public/timeline.json').read_text())
sr=48000
seconds=cfg['durationFrames']/cfg['fps']
rng=np.random.default_rng(cfg['seed'])
N=int(seconds*sr)
master=np.zeros((N,2),np.float64)

def add(sig,at,amp=.2,pan=0):
    i=round(at*sr); n=min(len(sig),N-i)
    if n<=0:return
    angle=(pan+1)*math.pi/4
    master[i:i+n,0]+=sig[:n]*amp*math.cos(angle)
    master[i:i+n,1]+=sig[:n]*amp*math.sin(angle)

def tone(freq,duration=.7):
    t=np.arange(round(duration*sr))/sr
    attack=1-np.exp(-t*500)
    return attack*np.exp(-t*5)*(np.sin(2*np.pi*freq*t)+.24*np.sin(2*np.pi*freq*2.003*t)+.11*np.sin(2*np.pi*freq*3*t))

def sweep(duration=.55):
    t=np.arange(round(duration*sr))/sr
    noise=rng.normal(0,1,len(t));noise=np.convolve(noise,np.ones(13)/13,'same')
    env=np.sin(np.pi*t/duration)**2
    return .6*noise*env+.12*np.sin(2*np.pi*(180*t+300*t*t))*env

def thump(duration=.35):
    t=np.arange(round(duration*sr))/sr
    freq=58+80*np.exp(-t*40)
    return np.sin(2*np.pi*np.cumsum(freq)/sr)*np.exp(-t*18)*(1-np.exp(-t*1300))

# Six four-second harmonic phrases. A soft downbeat and independent offbeat plucks.
chords=[[146.832,220,293.665],[130.813,196,261.626],[116.541,174.614,233.082],[130.813,196,261.626],[146.832,220,329.628],[146.832,220,293.665]]
for bar in range(6):
    freqs=chords[bar]
    for k in range(8):
        at=bar*4+k*.5
        # A brief gap around the snap lets that event read.
        level=.055 if not (7.8<=at<=9.3) else .013
        if bar==5:level*=.70
        add(thump(),at,level,0)
        if k in [0,3,5,7]:
            add(tone(freqs[(k+bar)%3]*2,1.3),at+.25,.043 if bar!=2 else .025,(-.3 if k%2 else .3))
    t=np.arange(int(4*sr))/sr
    env=np.sin(np.pi*t/4)**.7
    pad=sum(np.sin(2*np.pi*v*t+p*.23) for p,v in enumerate(freqs))/3
    add(pad*env,bar*4,.035,0)

report=[]
for e in cfg['events']:
    at=e['frame']/cfg['fps'];kind=e['kind'];pan=e['pan']
    if kind=='snap':
        t=np.arange(int(.27*sr))/sr
        noise=rng.normal(0,1,len(t))
        sig=noise*np.exp(-t*65)*.45+np.sin(2*np.pi*184*t)*np.exp(-t*23)*.35
        # A 1 ms attack eliminates an encoding-unfriendly discontinuity.
        sig*=np.minimum(1,t/.001)
        add(sig,at,.34,pan)
    elif kind=='sweep':add(sweep(),at-.12,.28,pan)
    elif kind=='tap':add(tone(440 if e['id']=='router' else 587.33,.4),at,.14,pan)
    elif kind=='pluck':add(tone(293.665,.65),at,.18,pan)
    elif kind=='resolve':
        for j,v in enumerate([293.665,440,587.33]):add(tone(v,2.1),at+j*.027,.14,pan-j*.2)
        add(thump(),at,.1,pan)
    elif kind=='bloom':
        for j,v in enumerate([220,293.665,440]):add(tone(v,1.4),at+j*.045,.09,pan-j*.15)
    report.append({**e,'seconds':at,'sample':round(at*sr)})
# Fade opening and tail; preserve the full planned duration.
master[:int(.08*sr)]*=np.linspace(0,1,int(.08*sr))[:,None]
master[-int(.85*sr):]*=np.linspace(1,0,int(.85*sr))[:,None]
peak=np.max(np.abs(master));master*=.72/peak
pcm=(master*32767).astype('<i2')
with wave.open(str(root/'public/soundtrack.wav'),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
(root/'evidence/audio-events.json').write_text(json.dumps({'sampleRate':sr,'duration':seconds,'samplePeakDBFS':20*np.log10(np.max(np.abs(master))),'events':report},indent=2))
# Subtle code-generated grain, with fixed seed; no external image is used.
noise=rng.normal(0,.8,(540,960,1))
base=np.array([253,251,247])[None,None,:]+noise
Image.fromarray(np.uint8(np.clip(base,0,255))).resize((1920,1080),Image.Resampling.BICUBIC).save(root/'public/paper.png')
print(json.dumps({'duration':seconds,'sampleRate':sr,'peakDBFS':20*np.log10(np.max(np.abs(master))),'events':len(report)}))
