import concurrent.futures
import json
import pathlib
import re
import shutil
import subprocess
import time

base = pathlib.Path(__file__).resolve().parent
info = json.loads((base / 'original.info.json').read_text())
parts = base / 'download-parts'
parts.mkdir(exist_ok=True)
chunk = 4 * 1024 * 1024
streams = {}
jobs = []
for name, format_id in [('video', '137'), ('audio', '140')]:
    fmt = next(f for f in info['formats'] if f['format_id'] == format_id)
    streams[name] = fmt
    for start in range(0, fmt['filesize'], chunk):
        end = min(start + chunk, fmt['filesize']) - 1
        jobs.append((name, start, end, fmt))

def fetch(job):
    name, start, end, fmt = job
    dest = parts / f'{name}-{start:012d}.part'
    expected = end - start + 1
    if dest.exists() and dest.stat().st_size == expected:
        return
    temp = dest.with_suffix('.transfer')
    headers = dest.with_suffix('.headers')
    partial = dest.with_suffix('.partial')
    if temp.exists() and headers.exists() and not partial.exists():
        prior = re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)', headers.read_text(errors='replace'), re.I)
        if prior and tuple(map(int, prior[-1])) == (start, end, fmt['filesize']) and temp.stat().st_size <= expected:
            temp.replace(partial)
    for attempt in range(3):
        have = partial.stat().st_size if partial.exists() else 0
        if have == expected:
            partial.replace(dest)
            return
        args = ['curl', '-4', '-sS', '-L', '--fail', '--connect-timeout', '15',
                '--max-time', '600', '--range', f'{start+have}-{end}', '-D', str(headers),
                '-o', str(temp)]
        for key, value in fmt.get('http_headers', {}).items():
            args += ['-H', f'{key}: {value}']
        result = subprocess.run(args + [fmt['url']], capture_output=True)
        raw_headers = headers.read_text(errors='replace') if headers.exists() else ''
        ranges = re.findall(r'content-range:\s*bytes\s+(\d+)-(\d+)/(\d+)', raw_headers, re.I)
        valid_range = ranges and tuple(map(int, ranges[-1])) == (start+have, end, fmt['filesize'])
        if valid_range and temp.exists() and temp.stat().st_size <= expected-have:
            with partial.open('ab') as out, temp.open('rb') as inp:
                shutil.copyfileobj(inp, out)
            temp.unlink()
            if partial.stat().st_size == expected:
                partial.replace(dest)
                return
    raise RuntimeError(f'{name} range {start}-{end} failed validation, exit={result.returncode}')

t = time.monotonic()
done = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
    for future in concurrent.futures.as_completed(pool.submit(fetch, job) for job in jobs):
        future.result()
        done += 1
        if done % 8 == 0 or done == len(jobs):
            print(f'Validated {done}/{len(jobs)} ranges in {time.monotonic()-t:.1f}s', flush=True)

for name, fmt in streams.items():
    stream_path = base / f'original-{name}.mp4'
    with stream_path.open('wb') as out:
        for start in range(0, fmt['filesize'], chunk):
            with (parts / f'{name}-{start:012d}.part').open('rb') as source:
                shutil.copyfileobj(source, out)
    assert stream_path.stat().st_size == fmt['filesize']

output = base.parent / 'original-interview-1080p.mp4'
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-n',
                '-i', str(base/'original-video.mp4'), '-i', str(base/'original-audio.mp4'),
                '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart',
                str(output)], check=True)
print(f'Completed: {output.name}, {output.stat().st_size} bytes', flush=True)
