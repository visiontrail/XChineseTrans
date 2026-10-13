import concurrent.futures
import hashlib
import json
import pathlib
import time
import urllib.request

ROOT = pathlib.Path(__file__).parent
INFO = json.loads((ROOT / 'test-video-cnc-mirror.info.json').read_text())
CHUNK = 1024 * 1024
FORMATS = {f['format_id']: f for f in INFO['formats']}


def download(fmt_id, extension):
    fmt = FORMATS[fmt_id]
    total = fmt['filesize']
    chunk_dir = ROOT / ('ranges-' + fmt_id)
    chunk_dir.mkdir(exist_ok=True)
    ranges = [(start, min(start + CHUNK - 1, total - 1)) for start in range(0, total, CHUNK)]

    def get_chunk(pair):
        start, end = pair
        path = chunk_dir / str(start)
        expected = end - start + 1
        # Earlier chunks in this ongoing task were written only after the exact
        # 206 Content-Range and expected byte count checks below had passed.
        if path.exists() and path.stat().st_size == expected:
            data = path.read_bytes()
            return {'start': start, 'end': end, 'bytes': len(data),
                    'range': f'bytes {start}-{end}/{total}', 'reused_in_same_task': True,
                    'sha256': hashlib.sha256(data).hexdigest()}
        headers = fmt.get('http_headers', INFO.get('http_headers', {})).copy()
        headers['Range'] = f'bytes={start}-{end}'
        for attempt in range(3):
            try:
                req = urllib.request.Request(fmt['url'], headers=headers)
                with urllib.request.urlopen(req, timeout=60) as response:
                    actual_range = response.headers.get('Content-Range')
                    assert response.status == 206, response.status
                    assert actual_range == f'bytes {start}-{end}/{total}', actual_range
                    data = response.read(expected + 1)
                assert len(data) == expected, (len(data), expected)
                path.write_bytes(data)
                return {'start': start, 'end': end, 'bytes': len(data), 'range': actual_range,
                        'sha256': hashlib.sha256(data).hexdigest()}
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(attempt + 1)

    checks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = {executor.submit(get_chunk, pair): pair for pair in ranges}
        for future in concurrent.futures.as_completed(futures):
            checks.append(future.result())
            if len(checks) % 16 == 0 or len(checks) == len(ranges):
                print(f'Format {fmt_id}: {len(checks)}/{len(ranges)} ranges verified', flush=True)
    out = ROOT / ('source-' + fmt_id + '.' + extension)
    with out.open('wb') as dest:
        for start, _ in ranges:
            dest.write((chunk_dir / str(start)).read_bytes())
    assert out.stat().st_size == total
    return {'format_id': fmt_id, 'media_url': fmt['url'], 'path': str(out), 'bytes': total,
            'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'ranges': sorted(checks, key=lambda x: x['start'])}


records = [download('136', 'mp4'), download('140', 'm4a')]
(ROOT / 'download-verification.json').write_text(json.dumps({
    'retrieved_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'source_page': INFO['webpage_url'], 'uploader': INFO['uploader'],
    'source_origin': 'Dongchedi test footage, mirrored by CarNewsChina; first-party file not recovered',
    'assets': records,
}, indent=2))
print('All files assembled and hashed', flush=True)
