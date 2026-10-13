from pathlib import Path
import concurrent.futures,subprocess,json,hashlib,datetime
p=Path(__file__).parent; total=2616562;step=262144
url='https://video.twimg.com/amplify_video/2107890134603481088/vid/avc1/3840x2160/KakPq_aXsoFB9L23.mp4?tag=29'
def complete(start):
 f=p/f'range-{start}.bin';end=min(start+step,total)-1
 h=p/f'range-{start}.headers'
 assert f'content-range: bytes {start}-{end}/{total}' in h.read_text().lower()
 n=f.stat().st_size
 if n<end-start+1:
  a=start+n; tail=p/f'tail-{a}.bin';th=p/f'tail-{a}.headers'
  subprocess.run(['curl','-L','--fail','--max-time','30','-sS','-r',f'{a}-{end}','-D',str(th),url,'-o',str(tail)],check=True)
  assert f'content-range: bytes {a}-{end}/{total}' in th.read_text().lower()
  assert tail.stat().st_size==end-a+1
  with f.open('ab') as w:w.write(tail.read_bytes())
 assert f.stat().st_size==end-start+1
 return f
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:files=list(ex.map(complete,range(0,total,step)))
out=p/'haiku-5-5-verified-original.mp4'
with out.open('wb') as w:
 for f in files:w.write(f.read_bytes())
r={'url':url,'source_post':'https://x.com/claudeai/status/2107894039626277339','retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'ranges_verified':True}
(p/'media-download.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
