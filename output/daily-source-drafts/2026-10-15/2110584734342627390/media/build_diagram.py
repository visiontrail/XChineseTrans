from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1600,1600),'#FDFBF7'); d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def text(x,y,s,size=36,color='#1A4A3A',b=False):d.text((x,y),s,font=ImageFont.truetype(bold if b else font,size),fill=color)
text(100,80,'ByteDance Seed',32,'#80601B')
text(100,140,'Safety across the model lifecycle',56,b=True)
text(100,230,'Alignment & Preparedness  ·  10 planned research hires',31,'#426454')
d.line((100,305,1500,305),fill='#D4AF37',width=2)
rows=[('01','Train across stages','Pretraining, midtraining, supervised fine-tuning','and reinforcement learning'),('02','Test adversarially','Automated model-vs-model attack and defense','plus external professional testing'),('03','Respond to unknown risks','Monitoring, blocking and attribution','are part of the announced remit')]
for i,(num,title,l1,l2) in enumerate(rows):
 y=360+i*225
 text(100,y,num,32,'#80601B'); text(210,y,title,42,b=True)
 text(210,y+68,l1,30,'#426454');text(210,y+113,l2,30,'#426454')
d.line((100,1065,1500,1065),fill='#D4AF37',width=2)
text(100,1110,'The engineering question',32,'#80601B')
text(100,1170,'When a new failure appears,',44,b=True)
text(100,1230,'does it change the system?',44,b=True)
text(100,1320,'Evaluation cases  →  training or deployment decisions',31,'#426454')
text(100,1440,'Source: Seed announcement · 14 Oct 2026',23,'#426454')
text(100,1480,'A question for agent-system builders',22,'#426454')
text(1260,1515,'LeoGuoLabs',25)
im.save(p/'seed-safety-lifecycle-v1.png')
