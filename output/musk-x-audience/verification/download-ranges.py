import urllib.request, concurrent.futures, pathlib, hashlib, json, datetime
root=pathlib.Path(__file__).resolve().parent.parent
url='https://video.twimg.com/amplify_video/2055323270858297344/vid/avc1/1654x1080/fiGyf0uVOFqSulx2.mp4?tag=27'
size=7379026
parts=root/'verification'/'parts'; parts.mkdir(exist_ok=True)
def get(i):
 a=i*262144; b=min(size-1,a+262143)
 req=urllib.request.Request(url,headers={'Range':f'bytes={a}-{b}'})
 with urllib.request.urlopen(req,timeout=40) as response:
  data=response.read(); cr=response.headers.get('Content-Range')
  assert response.status==206 and cr==f'bytes {a}-{b}/{size}',(i,response.status,cr)
  assert len(data)==b-a+1,(i,len(data))
 (parts/f'{i:03}.bin').write_bytes(data)
 return {'part':i,'range':cr,'bytes':len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
 records=list(pool.map(get,range((size+262143)//262144)))
data=b''.join((parts/f'{i:03}.bin').read_bytes() for i in range(len(records)))
assert len(data)==size
(root/'source-video.mp4').write_bytes(data)
(root/'verification'/'download-record.json').write_text(json.dumps({'source_post':'https://x.com/cb_doge/status/2055323416002281824','media_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'parts':records},indent=2))
print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}))
