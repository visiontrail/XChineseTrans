import concurrent.futures, datetime, hashlib, json, subprocess
from pathlib import Path
import urllib.request

BASE = Path(__file__).resolve().parent.parent

def download(slug, name, resolution=None):
    tweet = json.loads((BASE/'research'/f'source-{slug}.json').read_text())['tweet']
    video = tweet['media']['videos'][0]
    url = video['url']
    if resolution:
        url = next(f['url'] for f in video['formats'] if resolution in f['url'])
    folder = BASE/'media'/f'{slug}-ranges'
    folder.mkdir(exist_ok=True)
    def get_range(start, end, total=None):
        req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    header = response.headers.get('Content-Range', '')
                    data = response.read()
                    expected = f'bytes {start}-{end}/'
                    if response.status != 206 or not header.startswith(expected) or len(data) != end-start+1:
                        raise ValueError(f'Invalid range: {header} {len(data)}')
                    actual_total = int(header.split('/')[1])
                    if total is not None and total != actual_total:
                        raise ValueError('Total length changed')
                    (folder/f'{start:010}.bin').write_bytes(data)
                    return actual_total
            except Exception:
                if attempt == 2:
                    raise
    size = get_range(0, 131071)
    spans = [(s, min(s+131071, size-1)) for s in range(131072, size, 131072)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        list(pool.map(lambda span: get_range(*span, size), spans))
    dest = BASE/'media'/name
    data = b''.join(p.read_bytes() for p in sorted(folder.glob('*.bin')))
    assert len(data) == size
    dest.write_bytes(data)
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dest)]))
    decode = subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True)
    (BASE/'research'/f'{slug}-probe.json').write_text(json.dumps(probe,indent=2))
    (BASE/'research'/f'{slug}-decode.log').write_text(decode.stderr)
    record = {'source':tweet['url'],'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':size,'sha256':hashlib.sha256(data).hexdigest(),'path':str(dest),'range_validation':True,'decode_exit':decode.returncode,'decode_errors':decode.stderr,'duration':probe['format']['duration']}
    (BASE/'research'/f'{slug}-download.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(record), flush=True)

download('alexis', 'alexis-original-92s.mp4')
download('anatoli', 'source-clip-22s-720p.mp4', '/720x720/')
