import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
video = json.loads((root / 'research/source-vaibhav.json').read_text())['tweet']['media']['videos'][0]
url = video['url']
total = 26537537
size = 524288
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
parts = root / 'verification/parts'
parts.mkdir(exist_ok=True)

def grab(start):
    end = min(start + size, total) - 1
    expected = f'bytes {start}-{end}/{total}'
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
            with urllib.request.urlopen(req, timeout=18) as response:
                data = response.read()
                received = response.headers.get('Content-Range')
                assert response.status == 206 and received == expected and len(data) == end-start+1, (response.status, received, len(data))
            (parts / f'{start:010d}.part').write_bytes(data)
            return {'start':start, 'end':end, 'content_range':received, 'bytes':len(data)}
        except Exception:
            if attempt == 2:
                raise

starts = list(range(0, total, size))
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    receipts = []
    for receipt in pool.map(grab, starts):
        receipts.append(receipt)
        if len(receipts) % 10 == 0 or len(receipts) == len(starts):
            print(f'Validated {len(receipts)}/{len(starts)} ranges', flush=True)
out = root / 'media/sinclair-wgs-source-175s-1080p.mp4'
h = hashlib.sha256()
with out.open('wb') as destination:
    for start in starts:
        data = (parts / f'{start:010d}.part').read_bytes()
        destination.write(data)
        h.update(data)
assert out.stat().st_size == total
record = {'source_post':'https://x.com/VaibhavSisinty/status/2107825898502398376', 'media_url':url, 'started_at_utc':started, 'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'file':str(out), 'bytes':total, 'sha256':h.hexdigest(), 'range_validation':receipts}
(root / 'verification/download-record.json').write_text(json.dumps(record, indent=2))
print(json.dumps({k:v for k,v in record.items() if k != 'range_validation'}), flush=True)
