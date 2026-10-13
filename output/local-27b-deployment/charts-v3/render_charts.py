from pathlib import Path
import json, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

P=Path(__file__).resolve().parent
D=json.loads((P/'chart-data.json').read_text())
W,H=1600,2000
IVORY='#FDFBF7'; GREEN='#1A4A3A'; MUTED='#426454'; GOLD='#80601B'; ACCENT='#E5C158'; RULE='#CAD4CB'
fontpath=P/'Inter.ttf'
FP=FontProperties(fname=str(fontpath))
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Inter','DejaVu Sans'],'text.color':GREEN,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED,'font.size':20,'axes.unicode_minus':False})
FONTS={}
def font(size,weight=400):
    key=(size,weight)
    if key not in FONTS:
        f=ImageFont.truetype(str(fontpath),size)
        if hasattr(f,'set_variation_by_axes'):
            f.set_variation_by_axes([14,weight])
        FONTS[key]=f
    return FONTS[key]
def canvas():
    rng=np.random.default_rng(2710)
    base=np.empty((H,W,3),dtype=float);base[:]=[253,251,247]
    base+=rng.normal(0,0.24,(H,W,1))
    return Image.fromarray(np.clip(base,0,255).astype('uint8'))
def text(im,x,y,s,size=40,color=GREEN,weight=400,width=None,linegap=10):
    dr=ImageDraw.Draw(im); f=font(size,weight)
    lines=[]
    for paragraph in s.split('\n'):
        line=''
        for word in paragraph.split(' '):
            test=(line+' '+word).strip()
            if width and dr.textlength(test,font=f)>width and line:
                lines.append(line);line=word
            else:line=test
        lines.append(line)
    for line in lines:
        assert dr.textlength(line,font=f)<=W-x-65, (s,x,size)
        dr.text((x,y),line,font=f,fill=color,anchor='lt')
        y+=size+linegap
    return y

def rule(im,y):ImageDraw.Draw(im).line((96,y,1504,y),fill=RULE,width=2)
def title(im,kicker,headline,sub):
    text(im,96,84,kicker,30,GOLD,500)
    text(im,96,150,headline,83,GREEN,600)
    text(im,96,265,sub,38,MUTED)

def footer(im,n,source,notes):
    rule(im,1795)
    text(im,96,1830,notes,29,MUTED,width=1380,linegap=10)
    text(im,96,1925,f'{n} / 3',28,GOLD,500)
    text(im,265,1925,source,26,MUTED)
    dr=ImageDraw.Draw(im);sig='LeoGuoLabs';x=1504-dr.textlength(sig,font=font(30,500));text(im,x,1925,sig,30,GREEN,500)

def paste_plot(im,fig,xy):
    b=io.BytesIO();fig.savefig(b,format='png',dpi=100,transparent=True);plt.close(fig)
    b.seek(0);layer=Image.open(b).convert('RGBA');im.paste(layer,xy,layer)

def clean(ax):
    ax.set_facecolor('none')
    for side in ['top','right','left']:ax.spines[side].set_visible(False)
    ax.spines['bottom'].set_color(RULE)
    ax.tick_params(length=0,pad=10)
    ax.grid(axis='x',color=RULE,linewidth=.8,alpha=.55)
    ax.set_axisbelow(True)
    for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_fontproperties(FP);t.set_fontsize(24)

# 1: exact file-size bar chart plus open planning table.
im=canvas();title(im,'01 / HARDWARE & MEMORY','27B: what can run it?','Qwen3.6-27B · practical planning targets')
text(im,96,350,'Actual GGUF file sizes · decimal GB',44,GREEN,600)
fig,ax=plt.subplots(figsize=(14.4,3.8));fig.subplots_adjust(left=.17,right=.85,bottom=.21,top=.98)
labels=list(D['files']);vals=list(D['files'].values())
ax.barh(range(3),vals,color=[GREEN,MUTED,ACCENT],height=.57)
ax.set_yticks(range(3),labels);ax.invert_yaxis();ax.set_xlim(0,32);ax.set_xticks([0,10,20,30]);clean(ax)
for i,v in enumerate(vals):ax.text(v+.6,i,f'{v:.1f} GB',va='center',fontproperties=FP,fontsize=27,color=GREEN)

paste_plot(im,fig,(80,420))
text(im,96,822,'Add context cache + buffers + OS headroom.',32,MUTED)
rule(im,888);text(im,96,922,'Example setup',33,GOLD,500);text(im,770,922,'Starting point',33,GOLD,500)
rows=[
('16 GB GPU + 64 GB RAM','RTX 5060 Ti 16 GB','Smaller quant or CPU offload','Q4 can be tight'),
('24 GB GPU + 64 GB RAM','RTX 3090 / 4090 / RX 7900 XTX','Q4 / Q5 candidates','Check context + backend support'),
('32 GB GPU + 64 GB RAM','RTX 5090','More Q4 / Q5 headroom','Q8 leaves limited cache space'),
('2 × 24 GB GPU + 64 GB RAM','Dual RTX 3090','Split model / batch requests','Multi-GPU runtime required'),
('64 GB unified memory','Apple silicon Mac','Q4 / Q8 candidates','Shared with macOS + other apps')]
for i,(a,b,c,e) in enumerate(rows):
    y=995+i*150
    text(im,96,y,a,43,GREEN,600);text(im,96,y+60,b,32,MUTED)
    text(im,770,y,c,41,GREEN,500);text(im,770,y+60,e,32,MUTED)
    if i<4:rule(im,y+118)
text(im,96,1730,'RAM targets are a planning choice; speed is measured separately.',29,GOLD)
footer(im,1,'Files: Unsloth · 10 Oct 2026','Targets, not fit guarantees. Exact quant, context and runtime decide memory use.')
im.save(P/'01-configurations-v1.png')

# 2: concurrency with precise aggregate and per-stream distinctions.
im=canvas();title(im,'02 / A REPORTED DESKTOP TEST','More jobs, more throughput','2 × RTX 3090 · Ryzen 7 9800X3D · 64 GB DDR5')
text(im,96,350,'Qwen3.6-27B · AWQ INT4 · vLLM 0.21.0',37,GREEN,500)
text(im,96,412,'MTP-2 · FP8 KV cache · PCIe 4 ×8 / ×8 · no NVLink',31,MUTED)
fig,ax=plt.subplots(figsize=(14.6,7.4));fig.subplots_adjust(left=.12,right=.97,bottom=.15,top=.98)
x=np.arange(3);b=.28
ax.bar(x-b/2,D['concurrency']['aggregate_tps'],width=b,color=GREEN,label='Aggregate')
ax.bar(x+b/2,D['concurrency']['per_stream_tps'],width=b,color=ACCENT,label='Per-stream average')
ax.set_ylim(0,285);ax.set_yticks([0,50,100,150,200,250]);ax.set_xticks(x,['1 request','2 requests','4 requests'])
for spine in ['right','top','left']:ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color(RULE);ax.tick_params(length=0,pad=14);ax.grid(axis='y',color=RULE,linewidth=.8,alpha=.55);ax.set_axisbelow(True)
for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_fontproperties(FP);t.set_fontsize(23)
for series,shift in [(D['concurrency']['aggregate_tps'],-b/2),(D['concurrency']['per_stream_tps'],b/2)]:
    for i,v in enumerate(series):ax.text(i+shift,v+7,f'{v:.1f}',ha='center',fontproperties=FP,fontsize=27,color=GREEN)
ax.set_ylabel('Tokens / second',fontproperties=FP,fontsize=24,labelpad=14)
paste_plot(im,fig,(70,540))
dr=ImageDraw.Draw(im);dr.rectangle((96,486,130,510),fill=GREEN);text(im,146,480,'Aggregate',30,GREEN)
dr.rectangle((520,486,554,510),fill=ACCENT);text(im,570,480,'Per-stream average',30,GREEN)
rule(im,1350)
text(im,96,1400,'At 4 concurrent requests',35,MUTED)
text(im,96,1465,'255.9',89,GREEN,600);text(im,96,1574,'tok/s across all requests',33,MUTED)
text(im,855,1465,'65.6',89,GOLD,600);text(im,855,1574,'tok/s per stream, on average',31,MUTED)
text(im,96,1690,'More total output. Each stream slows down.',40,GREEN,600)
footer(im,2,'Reported: Ruashots · 26 May 2026','Short JSON prompts (~25 input tokens); output cap ~1,024 tokens; thinking off.\nCommunity measurement. Long-context and other tasks may differ.')
im.save(P/'02-concurrency-v1.png')

# 3: context depth, real line plots with separate scales and error bars.
im=canvas();title(im,'03 / A REPORTED MAC TEST','Context changes the speed','Apple M5 Max · 128 GB unified memory · Qwen3.6-27B')
text(im,96,350,'Q8_0 weights + Q8_0 KV cache · llama.cpp / Metal',35,GREEN,500)
text(im,96,412,'Flash Attention on · GPU layers 99 · 6 threads · 3 repeats',30,MUTED)
xs=np.array(D['context']['depth_tokens'])/1024

def line_panel(y,title_,vals,errs,color,ylim,ticks):
    text(im,96,y,title_,43,GREEN,600)
    fig,ax=plt.subplots(figsize=(14.5,4.6));fig.subplots_adjust(left=.13,right=.93,bottom=.22,top=.96)
    ax.errorbar(xs,vals,yerr=errs,color=color,linewidth=3.5,marker='o',markersize=9,capsize=4)
    ax.set_xlim(-8,270);ax.set_ylim(0,ylim);ax.set_xticks(xs,['0','32K','64K','128K','256K']);ax.set_yticks(ticks)
    for side in ['top','right']:ax.spines[side].set_visible(False)
    for side in ['bottom','left']:ax.spines[side].set_color(RULE)
    ax.tick_params(length=0,pad=10);ax.grid(axis='y',color=RULE,linewidth=.8,alpha=.55)
    for t in ax.get_xticklabels()+ax.get_yticklabels():t.set_fontproperties(FP);t.set_fontsize(23)
    ax.set_xlabel('Populated context depth (tokens)',fontproperties=FP,fontsize=23,labelpad=10)
    ax.set_ylabel('Tokens / second',fontproperties=FP,fontsize=22,labelpad=15)
    for x,v in zip(xs,vals):ax.annotate(f'{v:.2f}',(x,v),xytext=((10 if x==0 else 0),13),textcoords='offset points',ha=('left' if x==0 else 'center'),fontproperties=FP,fontsize=24,color=GREEN)
    paste_plot(im,fig,(65,y+66))
line_panel(500,'Generating the reply · TG256',D['context']['tg256_tps'],D['context']['tg_error'],GREEN,21,[0,5,10,15,20])
line_panel(1110,'Processing the next prompt · PP512',D['context']['pp512_tps'],D['context']['pp_error'],GOLD,970,[0,200,400,600,800])
text(im,96,1695,'17.46 → 4.27 tok/s as context fills to 256K',39,GREEN,600)
footer(im,3,'Reported: jyxjjj · 18 Aug 2026','One community run; build unspecified. TG256 generates 256 tokens; PP512 reads 512.\nDifferent quant and engine from image 2; these are separate tests.')
im.save(P/'03-context-speed-v1.png')

# Inspection sheet only; not a selected publishing attachment.
imgs=[Image.open(P/f) for f in ['01-configurations-v1.png','02-concurrency-v1.png','03-context-speed-v1.png']]
contact=Image.new('RGB',(1440,600),IVORY)
for i,img in enumerate(imgs):contact.paste(img.resize((480,600),Image.Resampling.LANCZOS),(i*480,0))
contact.save(P/'inspection-sheet.jpg')
print('Rendered 3 charts at 1600 x 2000 pixels.')
