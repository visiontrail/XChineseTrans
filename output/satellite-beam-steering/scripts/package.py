from pathlib import Path
import json,hashlib,re,shutil,zipfile,runpy
root=Path(__file__).resolve().parent.parent
render=json.loads((root/'evidence/render.json').read_text())
master=json.loads((root/'evidence/master.json').read_text())
p=root/'article.md';s=p.read_text();s=re.sub(r'The successful render took [0-9.]+ seconds and mastering took [0-9.]+ seconds',f"The successful render took {render['seconds']:.2f} seconds and mastering took {master['seconds']:.2f} seconds",s);p.write_text(s)
(root/'article.txt').write_text(s)
runpy.run_path(str(root/'scripts/build-article.py'),run_name='__main__')
old=root.parent/'codex-motion-routing'
if old.exists():
 for ext in ('md','txt','html'):
  p=old/f'article.{ext}';backup=old/f'article-v1.{ext}'
  if p.exists() and not backup.exists():shutil.copyfile(p,backup)
  s=(root/f'article.{ext}').read_text()
  if ext=='html':
   s=re.sub(r'(href|src)="(?!https?://|#)([^"]+)"',lambda m:f'{m[1]}="../satellite-beam-steering/{m[2]}"',s).replace('url(public/','url(../satellite-beam-steering/public/')
  p.write_text(s)
mp4=root/'steering-without-turning.mp4'
manifest=json.loads((root/'delivery.json').read_text());manifest.update(bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),render_seconds=render['seconds'],mastering_seconds=master['seconds'])
(root/'delivery.json').write_text(json.dumps(manifest,indent=2))
archive=root/'satellite-beam-steering-project.zip'
items=[]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(root.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(root)
  if any(p in ('node_modules','.bundle','.git') for p in rel.parts) or (f.suffix=='.zip' and f.name!='video-director.zip') or f.name=='.DS_Store':continue
  if f.name=='steering-without-turning-v1.mp4':continue
  if rel.parts[0]=='research' and (f.suffix.lower() in ('.mp4','.jpg','.png') or f.name.startswith('previous-routing')):continue
  z.write(f,Path(root.name)/rel);items.append(str(rel))
with zipfile.ZipFile(archive) as z:
 bad=z.testzip()
 if bad:raise RuntimeError(bad)
 required=['src/Film.tsx','src/Models.tsx','src/motion.ts','public/soundtrack.wav','package-lock.json','steering-without-turning.mp4','article.html','evidence/browser-playback.json','research/frame-audit-zh.md']
 for f in required:assert f in items,f
print(json.dumps({'archive':str(archive),'files':len(items),'bytes':archive.stat().st_size,'video':manifest},indent=2))
