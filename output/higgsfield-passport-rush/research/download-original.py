import concurrent.futures, json, pathlib, subprocess, time, shutil
base=pathlib.Path(__file__).resolve().parent
p=json.loads((base/'original-post.json').read_text())
url=next(v['url'] for v in p['tweet']['media']['videos'][0]['formats'] if '/1920x1080/' in v['url'])
total=448171054
chunk=4*1024*1024
parts=base/'download-parts'; parts.mkdir(exist_ok=True)
def fetch(i):
 start=i*chunk; end=min(total,start+chunk)-1; path=parts/f'{i:04d}.part'
 for attempt in range(4):
  have=path.stat().st_size if path.exists() else 0
  if have==end-start+1:return i
  if have>end-start+1: raise RuntimeError('Unexpected part size')
  tmp=path.with_suffix('.transfer')
  result=subprocess.run(['curl','-4','-sS','-L','--fail','--connect-timeout','15','--max-time','150','--range',f'{start+have}-{end}',url,'-o',str(tmp)],capture_output=True,text=True)
  if tmp.exists():
   n=tmp.stat().st_size
   if n>end-start+1-have:raise RuntimeError('Range ignored')
   with path.open('ab') as out, tmp.open('rb') as inp:shutil.copyfileobj(inp,out)
   tmp.unlink()
  if path.exists() and path.stat().st_size==end-start+1:return i
 raise RuntimeError(f'Part {i} incomplete: {result.stderr}')
n=(total+chunk-1)//chunk; done=0; t=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
 for result in concurrent.futures.as_completed([pool.submit(fetch,i) for i in range(n)]):
  result.result(); done+=1
  if done%8==0 or done==n: print(f'Downloaded {done}/{n} parts in {time.monotonic()-t:.1f}s',flush=True)
output=base.parent/'original-video-1080p.mp4'
with output.open('wb') as out:
 for i in range(n):
  with (parts/f'{i:04d}.part').open('rb') as inp:shutil.copyfileobj(inp,out)
assert output.stat().st_size==total
print('Complete:',output, total,flush=True)
