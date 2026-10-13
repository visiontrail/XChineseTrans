import concurrent.futures, pathlib, subprocess, re, json, hashlib, datetime

root = pathlib.Path(__file__).parent
url = json.loads((root/'source-original.json').read_text())['tweet']['media']['videos'][0]['url']
total = 48696251
chunk = 524288
parts = root/'download-parts'
parts.mkdir(exist_ok=True)

def get_part(index):
    start = index*chunk
    end = min(total-1, start+chunk-1)
    data = parts/f'{index:03d}.bin'
    headers = parts/f'{index:03d}.headers'
    h = headers.read_text().lower() if headers.exists() else ''
    size = data.stat().st_size if data.exists() else 0
    if size and (f'content-range: bytes {start}-{end}/{total}' not in h or size>end-start+1):
        raise RuntimeError(f'Cannot verify existing prefix for range {index}')
    requests = []
    while size < end-start+1:
        a = start+size
        b = min(end,a+65535)
        temp = parts/f'{index:03d}-resume.bin'
        hh = parts/f'{index:03d}-resume.headers'
        for attempt in range(4):
            r = subprocess.run(['curl','-L','--fail','--max-time','30','-sS','-H',f'Range: bytes={a}-{b}','-D',str(hh),url,'-o',str(temp)],capture_output=True)
            head = hh.read_text().lower() if hh.exists() else ''
            if r.returncode == 0 and temp.stat().st_size == b-a+1 and f'content-range: bytes {a}-{b}/{total}' in head:
                with data.open('ab') as out: out.write(temp.read_bytes())
                size += b-a+1
                requests.append({'start':a,'end':b,'bytes':b-a+1,'attempts':attempt+1})
                break
        else: raise RuntimeError(f'Resume range {a}-{b} failed: {r.stderr.decode()}')
    return {'index':index,'start':start,'end':end,'bytes':size,'resumed_ranges':requests}

count = (total+chunk-1)//chunk
records = []
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    for result in pool.map(get_part,range(count)):
        records.append(result)
        if len(records)%16==0: print(f'Validated {len(records)}/{count} ranges',flush=True)
target = root/'original-video-complete.mp4'
with target.open('wb') as out:
    for i in range(count): out.write((parts/f'{i:03d}.bin').read_bytes())
assert target.stat().st_size == total
record = {'source_post':'https://x.com/lennysan/status/2108652242215878775','media_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':total,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'ranges':records}
(root/'download-verification.json').write_text(json.dumps(record,indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='ranges'},indent=2),flush=True)
