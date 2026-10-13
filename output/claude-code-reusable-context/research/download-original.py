"""Download public original media in validated HTTP byte ranges."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import os
import time
import urllib.request

root = Path(__file__).resolve().parent.parent
research = root / 'research'
metadata = json.loads((research / 'source-video-post.json').read_text())
video = metadata['tweet']['media']['videos'][0]
main_url = max((item for item in video['formats'] if item.get('container') == 'mp4'), key=lambda item: item.get('bitrate', 0))['url']
jobs = [('original-video.mp4', main_url)]
chunk_size = 1024 * 1024
records = []
tasks = []
for name, url in jobs:
    with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=30) as response:
        total = int(response.headers['Content-Length'])
    temp = root / (name + '.part')
    with temp.open('wb') as stream:
        stream.truncate(total)
    record = {'name': name, 'url': url, 'bytes': total, 'temporary_path': str(temp)}
    records.append(record)
    for start in range(0, total, chunk_size):
        tasks.append((record, start, min(total - 1, start + chunk_size - 1)))

def fetch_chunk(task):
    record, start, end = task
    expected = end - start + 1
    for attempt in range(3):
        try:
            request = urllib.request.Request(record['url'], headers={
                'User-Agent': 'Mozilla/5.0', 'Range': f'bytes={start}-{end}'})
            with urllib.request.urlopen(request, timeout=45) as response:
                actual_range = response.headers.get('Content-Range')
                wanted_range = f"bytes {start}-{end}/{record['bytes']}"
                if response.status != 206 or actual_range != wanted_range:
                    raise ValueError(f'Unexpected range response: {response.status} {actual_range}')
                data = response.read()
            if len(data) != expected:
                raise ValueError(f'Expected {expected} bytes, got {len(data)}')
            with open(record['temporary_path'], 'r+b') as stream:
                stream.seek(start)
                stream.write(data)
            return len(data)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)

completed = 0
started = time.time()
with ThreadPoolExecutor(max_workers=24) as executor:
    for future in as_completed([executor.submit(fetch_chunk, task) for task in tasks]):
        completed += future.result()
        if completed // (10 * chunk_size) != (completed - chunk_size) // (10 * chunk_size):
            print(json.dumps({'downloaded_mb': round(completed / 1e6), 'seconds': round(time.time() - started)}), flush=True)
for record in records:
    temporary = Path(record.pop('temporary_path'))
    record['sha256'] = hashlib.file_digest(temporary.open('rb'), 'sha256').hexdigest()
    os.replace(temporary, root / record['name'])
    print(json.dumps(record), flush=True)
(research / 'verified-download-manifest.json').write_text(json.dumps(records, indent=2))
