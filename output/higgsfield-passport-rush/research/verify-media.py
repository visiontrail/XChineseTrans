import hashlib,json,pathlib,subprocess
base=pathlib.Path(__file__).resolve().parent
video=base.parent/'original-video-1080p.mp4'
assert video.stat().st_size==448171054
metadata=subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)],text=True)
(base/'video-metadata.json').write_text(metadata)
info=json.loads(metadata)
assert abs(float(info['format']['duration'])-1685.29)<0.1
assert {s['codec_type'] for s in info['streams']}=={'video','audio'}
v=next(s for s in info['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(1920,1080)
frames=base/'sampled-frames'; frames.mkdir(exist_ok=True)
# Decode the entire video and audio; save regularly spaced video frames for visual QA.
with (base/'decode.log').open('w') as log:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(video),'-map','0:v:0','-vf','fps=1/84,scale=640:-1','-fps_mode','vfr',str(frames/'frame-%02d.jpg'),'-map','0:a:0','-f','null','-'],check=True,stderr=log)
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-pattern_type','glob','-i',str(frames/'frame-*.jpg'),'-vf','scale=480:-1,tile=4x5','-frames:v','1',str(base/'contact-sheet.jpg')],check=True)
hashvalue=hashlib.file_digest(video.open('rb'),'sha256').hexdigest()
manifest={'status':'prepared_not_published','format':'standalone','account':'LeoGuoLabs','text':'post.txt','video':'original-video-1080p.mp4','video_source_post':'https://x.com/higgsfield_ai/status/2103570077325095208','original_youtube':'https://www.youtube.com/watch?v=reFzEtCG_m8','bytes':video.stat().st_size,'sha256':hashvalue,'duration_seconds':float(info['format']['duration']),'width':1920,'height':1080,'video_codec':v['codec_name'],'full_audio_video_decode':'passed','sampled_frames':len(list(frames.glob('*.jpg'))),'subtitle_streams':0,'visual_subtitle_check':'pending'}
(base.parent/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2),flush=True)
