import concurrent.futures,subprocess,pathlib,hashlib
p=pathlib.Path(__file__).resolve().parent
jobs=[('CC__Calendar.mp4',11623180,'13926aec765000719bbd23bfe4eb99c0','01-official-calendar.mp4'),('CC__Completing_Tasks.mp4',6788527,'4c5895e383ad414606d56ed188b680b4','02-official-tasks.mp4')]
parts=p/'parts';parts.mkdir(exist_ok=True)
def fetch(x):
 name,start,end=x;path=parts/(name+f'.{start}')
 for attempt in range(3):
  r=subprocess.run(['curl','-sS','-L','--connect-timeout','15','--max-time','60','--range',f'{start}-{end}','https://storage.googleapis.com/gweb-uniblog-publish-prod/original_videos/'+name,'-o',str(path)],capture_output=True)
  if r.returncode==0 and path.stat().st_size==end-start+1:return
 raise RuntimeError(str(x)+': '+r.stderr.decode())
chunks=[(name,start,min(start+262143,size-1)) for name,size,_,_ in jobs for start in range(0,size,262144)]
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
 for i,_ in enumerate(ex.map(fetch,chunks)): 
  if i%10==0:print('Parts complete',i+1,'/',len(chunks),flush=True)
for name,size,md5,out in jobs:
 data=b''.join((parts/(name+f'.{start}')).read_bytes() for start in range(0,size,262144))
 assert len(data)==size and hashlib.md5(data).hexdigest()==md5
 (p.parent/out).write_bytes(data)
 print('Verified',out,len(data),md5,flush=True)
