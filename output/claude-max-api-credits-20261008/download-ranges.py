from pathlib import Path
import concurrent.futures, subprocess,re,json,hashlib,datetime
p=Path(__file__).parent
url='https://video.twimg.com/amplify_video/2107890134603481088/vid/avc1/3840x2160/KakPq_aXsoFB9L23.mp4?tag=29'
total=2616562
step=262144
def get(start):
 end=min(start+step,total)-1
 f=p/f'range-{start}.bin'; h=p/f'range-{start}.headers'
 subprocess.run(['curl','-L','--fail','--max-time','40','-sS','-r',f'{start}-{end}','-D',str(h),url,'-o',str(f)],check=True)
 assert f.stat().st_size==end-start+1
 assert f'content-range: bytes {start}-{end}/{total}' in h.read_text().lower()
 return f
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 files=list(ex.map(get,range(0,total,step)))
out=p/'haiku-5-5-verified-original.mp4'
with out.open('wb') as w:
 for f in files:w.write(f.read_bytes())
record={'url':url,'source_post':'https://x.com/claudeai/status/2107894039626277339','retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'ranges_verified':True}
(p/'media-download.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record))
