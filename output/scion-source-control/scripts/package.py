import pathlib,zipfile,json,hashlib
p=pathlib.Path(__file__).resolve().parents[1]
roots=['src','public','scripts','research','evidence']
files=[p/f for f in ['README.md','post-en.txt','director-brief.md','shot-plan.md','script.json','narration.txt','captions.srt','review.html','poster.jpg','package.json','package-lock.json','requirements.txt','delivery.json','publication-record.json','scion-explained.mp4']]
for d in roots:
 files.extend(f for f in (p/d).rglob('*') if f.is_file() and '__pycache__' not in f.parts)
archive=p/'scion-explained-project.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,'scion-source-control/'+str(f.relative_to(p)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))
