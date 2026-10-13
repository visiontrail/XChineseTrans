import concurrent.futures
import hashlib
import json
import pathlib
import subprocess
from PIL import Image, ImageDraw

base = pathlib.Path(__file__).resolve().parent
video = base.parent / 'original-interview-1080p.mp4'
meta = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(video)]))
v = next(s for s in meta['streams'] if s['codec_type'] == 'video')
a = next(s for s in meta['streams'] if s['codec_type'] == 'audio')
assert (v['codec_name'], v['width'], v['height']) == ('h264', 1920, 1080)
assert a['codec_name'] == 'aac'
duration = float(meta['format']['duration'])
assert 1405 < duration < 1408

def frame(seconds):
    dest = base / f'frame-{seconds}.jpg'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(seconds),
                    '-i', str(video), '-frames:v', '1', '-vf', 'scale=720:-1', '-q:v', '2', str(dest)], check=True)
    return seconds, dest

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    frames = list(pool.map(frame, [10, 450, 900, 1390]))
sheet = Image.new('RGB', (1440, 858), '#FDFBF7')
draw = ImageDraw.Draw(sheet)
for i, (seconds, path) in enumerate(frames):
    x, y = (i % 2) * 720, (i // 2) * 429
    with Image.open(path) as image:
        sheet.paste(image, (x, y))
    draw.text((x+10, y+408), f'{seconds//60:02d}:{seconds%60:02d}', fill='#1A4A3A')
sheet.save(base.parent / 'video-preview.jpg', quality=92)
meta['sha256'] = hashlib.file_digest(video.open('rb'), 'sha256').hexdigest()
meta['sampled_frame_seconds'] = [x[0] for x in frames]
meta['source'] = 'https://www.youtube.com/watch?v=uD62Yn8j_Pg'
meta['assembly'] = 'Validated HTTP byte ranges; H.264 and AAC remuxed without re-encoding.'
(base / 'media-check.json').write_text(json.dumps(meta, indent=2)+'\n')
print(json.dumps({'duration':duration,'width':v['width'],'height':v['height'],'video_codec':v['codec_name'],
                  'audio_codec':a['codec_name'],'bytes':video.stat().st_size,'sha256':meta['sha256']}))
