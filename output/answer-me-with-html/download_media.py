import urllib.request,pathlib,json,concurrent.futures,hashlib,datetime,time
p=pathlib.Path(__file__).parent
sources=[('source-x-demo.mp4',json.loads((p/'source-post.json').read_text())['tweet']['media']['videos'][0]['url'],7747870),('creator-demo.mp4','https://github.com/user-attachments/assets/d3063a28-5dfd-4c44-a562-be901c49b249',8896036)]
logs=[]
def chunk(job):
 name,url,total,start,end=job
 expected=f'bytes {start}-{end}/{total}'
 for attempt in range(3):
  try:
   req=urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}'})
   with urllib.request.urlopen(req,timeout=20) as r:
    cr=r.headers.get('Content-Range'); data=r.read()
    assert r.status==206 and cr==expected and len(data)==end-start+1,(r.status,cr,len(data),expected)
   path=p/(name+f'.{start}.part'); path.write_bytes(data)
   logs.append({'file':name,'range':cr,'bytes':len(data)})
   print(name,start,len(data),flush=True)
   return path
  except Exception as exc:
   if attempt==2: raise
 jobs=None
for name,url,total in sources:
 jobs=[(name,url,total,start,min(total-1,start+524287)) for start in range(0,total,524288)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  parts=list(pool.map(chunk,jobs))
 target=p/name
 with target.open('wb') as f:
  for path in parts:f.write(path.read_bytes())
 assert target.stat().st_size==total
 logs.append({'file':name,'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':total,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 (p/'download-verification.json').write_text(json.dumps(logs,indent=2))
 print('COMPLETE',name,flush=True)
