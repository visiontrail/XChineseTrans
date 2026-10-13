import urllib.request,json,concurrent.futures,time,re,os
from pathlib import Path
root=Path(__file__).parent
manifest=[]
def fetch(url,path,total):
 chunksize=1048576
 def chunk(start):
  end=min(start+chunksize,total)-1
  p=root/(path.name+f'.chunk-{start}')
  expected=f'bytes {start}-{end}/{total}'
  for attempt in range(4):
   try:
    req=urllib.request.Request(url,headers={'Range':f'bytes={start}-{end}'})
    with urllib.request.urlopen(req,timeout=50) as response:
     cr=response.headers.get('Content-Range');data=response.read()
    if cr!=expected or len(data)!=end-start+1:raise ValueError((cr,len(data),expected))
    p.write_bytes(data)
    return p
   except Exception:
    if attempt==3:raise
    time.sleep(1)
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  paths=list(pool.map(chunk,range(0,total,chunksize)))
 with path.open('wb') as target:
  for p in paths:target.write(p.read_bytes())
 assert path.stat().st_size==total
 for p in paths:p.unlink()
 manifest.append({'path':str(path),'url':url,'bytes':total,'retrieved_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'all_ranges_verified':True})
 print(path.name,total,'verified',flush=True)
x=json.loads((root/'official-info.json').read_text())
for f in x['requested_formats']:
 fetch(f['url'],root/('official-'+f['format_id']+'.'+f['ext']),f['filesize'])
(root/'range-retrieval.json').write_text(json.dumps(manifest,indent=2))
