from pathlib import Path
import zipfile, json, hashlib
p=Path(__file__).resolve().parents[1]
video=p/'when-ai-becomes-the-research-team.mp4'; post=p/'post.txt'; report=json.loads((p/'evidence/final-check/delivery-check.json').read_text())
assert report['checks_passed']
manifest=dict(title='When AI becomes the research team',format='standalone X post with direct video attachment',account='@LeoGuoLabs',publication_status='awaiting_final_approval',video=video.name,video_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),post=post.name,post_sha256=hashlib.sha256(post.read_bytes()).hexdigest(),duration_seconds=report['format']['duration'],dimensions=[report['width'],report['height']],fps=report['fps'],decoded_frames=report['decoded_frames'],audio_measurement=report['audio_measurement'],review='review.html',sources='research/verification.md',qa='evidence/qa.md',editable_project='ai-research-feedback-project.zip')
(p/'delivery.json').write_text(json.dumps(manifest,indent=2)+'\n')
files=[x for x in p.rglob('*') if x.is_file() and not any(a in ['node_modules','.venv','.bundle','frames'] for a in x.relative_to(p).parts) and x.suffix!='.zip' and not x.name.startswith('research-feedback-') and not (x.parent.name=='research' and x.suffix in ['.mp4','.mp3','.json','.txt','.jpg'])]
with zipfile.ZipFile(p/'ai-research-feedback-project.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,'ai-research-feedback/'+str(f.relative_to(p)))
with zipfile.ZipFile(p/'ai-research-feedback-project.zip') as z:
 assert z.testzip() is None; print('Archive:',len(z.namelist()),'files')
print(json.dumps(manifest,indent=2))
