import urllib.request, concurrent.futures, json, datetime, hashlib, pathlib, time
root=pathlib.Path('output/musk-uhi-purpose')
url=json.load(open(root/'research/supplied-post.json'))['tweet']['media']['videos'][0]['url']
total=640282
chunk=65536

def get(item):
    i,start,end=item
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={'Range':f'bytes={start}-{end}'})
            with urllib.request.urlopen(req,timeout=18) as resp:
                cr=resp.headers.get('Content-Range'); data=resp.read()
                if resp.status!=206 or cr!=f'bytes {start}-{end}/{total}' or len(data)!=end-start+1:
                    raise ValueError((resp.status,cr,len(data)))
            (root/f'research/range-{i:02d}.bin').write_bytes(data)
            return {'part':i,'start':start,'end':end,'bytes':len(data),'content_range':cr}
        except Exception as e:
            if attempt==2: raise
    
parts=[(i,start,min(start+chunk-1,total-1)) for i,start in enumerate(range(0,total,chunk))]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records=list(pool.map(get,parts))
path=root/'media/musk-universal-high-income-original.mp4'
with path.open('wb') as out:
    for i,_,_ in parts: out.write((root/f'research/range-{i:02d}.bin').read_bytes())
data=path.read_bytes()
assert len(data)==total
record={'source_post':'https://x.com/GeniusGTX/status/2108724471792382279','supplied_post':'https://x.com/0x404page/status/2109510762771407042','url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'ranges':records}
(root/'verification/download-record.json').write_text(json.dumps(record,indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='ranges'},indent=2))
