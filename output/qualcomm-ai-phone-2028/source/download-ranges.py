import pathlib, json, concurrent.futures, subprocess, re, hashlib, datetime, time
root=pathlib.Path(__file__).resolve().parents[1]
j=json.load(open(root/'source/fireside.json'))['tweet']
a=j['quote']
jobs=[('source-clip-verified.mp4',j['media']['videos'][0]['url'],9125375,j['url']),('source/interview-full-720p-verified.mp4',next(f['url'] for f in a['media']['videos'][0]['formats'] if '1280x720' in f['url']),227499965,a['url'])]
records=[]
for name,url,total,post in jobs:
 folder=root/'source'/(pathlib.Path(name).stem+'-ranges'); folder.mkdir(exist_ok=True)
 chunk=524288
 parts=[(i,start,min(start+chunk-1,total-1)) for i,start in enumerate(range(0,total,chunk))]
 def get(part):
  i,start,end=part; dest=folder/f'{i:04d}.bin'; headers=folder/f'{i:04d}.headers'
  if dest.exists() and headers.exists():
   ranges=re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)',headers.read_text().lower())
   if ranges and tuple(map(int,ranges[-1]))==(start,end,total) and dest.stat().st_size==end-start+1:return {'part':i,'start':start,'end':end,'bytes':dest.stat().st_size}
  for attempt in range(4):
   r=subprocess.run(['curl','-L','--fail','--silent','--show-error','--max-time','75','--range',f'{start}-{end}','-D',str(headers),url,'-o',str(dest)],capture_output=True)
   ranges=re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)',headers.read_text().lower() if headers.exists() else '')
   if r.returncode==0 and ranges and tuple(map(int,ranges[-1]))==(start,end,total) and dest.stat().st_size==end-start+1:return {'part':i,'start':start,'end':end,'bytes':dest.stat().st_size}
  raise RuntimeError(f'Failed verified range {part}: {r.stderr.decode()}')
 started=time.time(); completed=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
  futures=[pool.submit(get,p) for p in parts]
  for f in concurrent.futures.as_completed(futures):
   completed.append(f.result())
   if len(completed)%32==0 or len(completed)==len(parts):print(name,len(completed),'/',len(parts),'parts',round(time.time()-started),'seconds',flush=True)
 dest=root/name
 with dest.open('wb') as out:
  for i,_,_ in parts:
   with (folder/f'{i:04d}.bin').open('rb') as inp:
    while buf:=inp.read(1048576):out.write(buf)
 assert dest.stat().st_size==total
 rec={'path':name,'source_post':post,'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':total,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'range_checks':sorted(completed,key=lambda p:p['part'])}
 records.append(rec); (root/'source/downloads-verified.json').write_text(json.dumps(records,indent=2)); print({k:v for k,v in rec.items() if k!='range_checks'},flush=True)
