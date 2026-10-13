from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import subprocess, re, json, hashlib, datetime, sys

ROOT = Path(__file__).resolve().parent
URL = 'https://about.fb.com/wp-content/uploads/2026/10/Researchers-Introducing-Muse-Wonder_header.mp4'
TOTAL = 41018340
config = json.loads((ROOT / sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
URL = config.get('url', URL)
TOTAL = config.get('bytes', TOTAL)
STEP = 1048576
parts = ROOT / config.get('parts_dir', 'official-download-parts')
parts.mkdir(exist_ok=True)

def acquire(i):
    start, end = i * STEP, min((i + 1) * STEP, TOTAL) - 1
    path, headers = parts / f'{i:03d}.bin', parts / f'{i:03d}.headers'
    h = headers.read_text() if headers.exists() else ''
    ranges = re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)', h, flags=re.I)
    if path.exists():
        assert ranges and tuple(map(int, ranges[-1])) == (start, end, TOTAL), f'part {i}: invalid retained range'
        assert path.stat().st_size <= end - start + 1
    else:
        path.write_bytes(b'')
    transfers = []
    for attempt in range(6):
        have = path.stat().st_size
        if have == end - start + 1:
            break
        offset = start + have
        tail, tail_headers = parts / f'{i:03d}.tail', parts / f'{i:03d}.tail.headers'
        result = subprocess.run(['curl', '-L', '--fail', '--max-time', '35', '-sS', '-r', f'{offset}-{end}', '-D', str(tail_headers), URL, '-o', str(tail)], capture_output=True, text=True)
        response_headers = tail_headers.read_text() if tail_headers.exists() else ''
        response_ranges = re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)', response_headers, flags=re.I)
        if not response_ranges:
            print(f'Part {i}: retry after transport failure', flush=True)
            continue
        assert tuple(map(int, response_ranges[-1])) == (offset, end, TOTAL), f'part {i}: invalid resumed range'
        if have == 0:
            headers.write_text(response_headers)
        payload = tail.read_bytes() if tail.exists() else b''
        assert len(payload) <= end - offset + 1
        if result.returncode == 0:
            assert len(payload) == end - offset + 1
        with path.open('ab') as dest:
            dest.write(payload)
        transfers.append({'start':offset,'end_received':offset+len(payload)-1,'bytes':len(payload),'content_range':response_ranges[-1],'curl_exit':result.returncode})
    assert path.stat().st_size == end - start + 1, f'part {i}: size mismatch'
    return {'part': i, 'start': start, 'end': end, 'bytes': path.stat().st_size, 'resumed_transfers':transfers, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

count = (TOTAL + STEP - 1) // STEP
first = acquire(0)
print('Range verified:', first['bytes'], flush=True)
verified = [first]
with ThreadPoolExecutor(max_workers=6) as pool:
    for future in as_completed([pool.submit(acquire, i) for i in range(1, count)]):
        verified.append(future.result())
        print(f'Verified {len(verified)}/{count}', flush=True)

out = ROOT / config.get('output', 'meta-official-full.mp4')
if out.exists():
    out.rename(out.with_suffix('.initial-partial.mp4'))
with out.open('wb') as dest:
    for i in range(count):
        dest.write((parts / f'{i:03d}.bin').read_bytes())
assert out.stat().st_size == TOTAL
record = {'source_page': config.get('source_page', 'https://about.fb.com/news/2026/10/introducing-muse-wonder-models/'), 'source_url': URL, 'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'bytes': TOTAL, 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'parts': sorted(verified, key=lambda r: r['part'])}
(ROOT / config.get('record', 'official-download-verification.json')).write_text(json.dumps(record, indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='parts'}), flush=True)
