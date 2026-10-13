from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parent.parent
files=sorted((p/'evidence').glob('beat-*.jpg'))
cols=6;w=384;h=248
im=Image.new('RGB',(cols*w,((len(files)+cols-1)//cols)*h),'#FDFBF7');d=ImageDraw.Draw(im)
for i,f in enumerate(files):
 x=(i%cols)*w;y=(i//cols)*h
 im.paste(Image.open(f),(x,y));d.text((x+10,y+221),f'{i*30:04d}f / {i*.5:04.1f}s',fill='#1a4a3a')
im.save(p/'evidence/beat-contact-sheet.jpg',quality=92)
keys=[90,330,540,870,1122,1350]
im=Image.new('RGB',(1440,584),'#FDFBF7');d=ImageDraw.Draw(im)
for i,f in enumerate(keys):
 x=i%3*480;y=i//3*292
 im.paste(Image.open(p/f'frames/frame-{f:04d}.png').resize((480,270)),(x,y));d.text((x+12,y+272),f'{f:04d}f / {f/60:.2f}s',fill='#1a4a3a')
im.save(p/'storyboard.jpg',quality=94)
print('beat samples:',len(files))
