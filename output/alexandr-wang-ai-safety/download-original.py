import concurrent.futures, pathlib, subprocess, re, json, hashlib, datetime

root = pathlib.Path(__file__).parent
media = json.loads((root/'source-cleoabram.json').read_text())['tweet']['media']['videos'][0]
url = next(f['url'] for f in media['formats'] if '/1280x720/' in f['url'])
total = 26250940
chunk = 65536
parts = root/'download-parts'
parts.mkdir(exist_ok=True)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch(i):
    start = i*chunk
    end = min(total-1, start+chunk-1)
    data, headers = parts/f'{i:04}.bin', parts/f'{i:04}.headers'
    for attempt in range(4):
        result = subprocess.run(['curl','-L','--fail','--max-time','25','-sS','-H',f'Range: bytes={start}-{end}','-D',str(headers),url,'-o',str(data)],capture_output=True)
        if result.returncode == 0 and data.stat().st_size == end-start+1 and f'content-range: bytes {start}-{end}/{total}' in headers.read_text().lower():
            return {'start':start,'end':end,'bytes':end-start+1}
    raise RuntimeError(f'Invalid range {start}-{end}: {result.stderr.decode()}')

count = (total+chunk-1)//chunk
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
    records = []
    for record in pool.map(fetch,range(count)):
        records.append(record)
        if len(records)%100==0: print(f'Validated {len(records)}/{count} ranges',flush=True)
target = root/'original-full-720p.mp4'
with target.open('wb') as out:
    for i in range(count): out.write((parts/f'{i:04}.bin').read_bytes())
assert target.stat().st_size == total
record = {'source_post':'https://x.com/cleoabram/status/2107989027223736462','media_url':url,'retrieved_at':started,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':total,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'ranges':records}
(root/'download-verification.json').write_text(json.dumps(record,indent=2))
print({k:v for k,v in record.items() if k!='ranges'},flush=True)
