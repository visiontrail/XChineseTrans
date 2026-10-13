import concurrent.futures, hashlib, json, pathlib, subprocess, time
root=pathlib.Path(__file__).resolve().parents[1]
url="https://video.twimg.com/amplify_video/2107153827468062720/vid/avc1/1280x720/pHC6kVqXst_zA2Gk.mp4?tag=29"
total=331202087
chunk=1048576
parts=root/"verification"/"parts720"
parts.mkdir(exist_ok=True)
started=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
def grab(i):
 a=i*chunk;b=min(a+chunk,total)-1
 dest=parts/f"{i:04d}.bin";hdr=parts/f"{i:04d}.headers"
 for attempt in range(4):
  r=subprocess.run(["curl","-L","--fail","--connect-timeout","10","--max-time","60","-sS","-H",f"Range: bytes={a}-{b}","-D",str(hdr),url,"-o",str(dest)],capture_output=True)
  headers=hdr.read_text() if hdr.exists() else ""
  if r.returncode==0 and dest.stat().st_size==b-a+1 and f"content-range: bytes {a}-{b}/{total}" in headers.lower():return i
 raise RuntimeError(f"Range {a}-{b} failed: {r.stderr.decode()}")
n=(total+chunk-1)//chunk
with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
 for count,idx in enumerate(pool.map(grab,range(n)),1):
  if count%20==0 or count==n:print(f"verified ranges {count}/{n}",flush=True)
out=root/"media"/"lauren-tan-session-65m-720p.mp4"
h=hashlib.sha256()
with out.open("wb") as f:
 for i in range(n):
  data=(parts/f"{i:04d}.bin").read_bytes();f.write(data);h.update(data)
assert out.stat().st_size==total
record={"source_post":"https://x.com/0xCodez/status/2107155830093078557","url":url,"retrieved_started_at":started,"retrieved_completed_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"bytes":total,"sha256":h.hexdigest(),"file":str(out),"ranges":n,"range_validation":"every Content-Range and byte count matched","source_caveat":"Reupload with modified background; not a clean original recording."}
(root/"verification"/"download.json").write_text(json.dumps(record,indent=2))
print(json.dumps(record),flush=True)
