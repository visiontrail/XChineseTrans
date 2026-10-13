from pathlib import Path
import json,hashlib,re,struct
root=Path(__file__).resolve().parent.parent
f=root/'route-around-failure.mp4'
j=json.loads((root/'evidence/final-ffprobe.json').read_text())
v=next(x for x in j['streams'] if x['codec_type']=='video');a=next(x for x in j['streams'] if x['codec_type']=='audio')
l=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',(root/'evidence/final-loudness.log').read_text()).group(0))
browser=json.loads((root/'evidence/browser-verification.json').read_text())
motion=json.loads((root/'evidence/motion-check.json').read_text())
links=json.loads((root/'evidence/link-check.json').read_text())
atoms=[]
with f.open('rb') as inp:
 while True:
  offset=inp.tell();b=inp.read(8)
  if len(b)<8:break
  size,tag=struct.unpack('>I4s',b)
  if size==1:size=struct.unpack('>Q',inp.read(8))[0]
  if size==0:break
  atoms.append({'type':tag.decode('ascii','replace'),'offset':offset,'size':size});inp.seek(offset+size)
faststart=next(x['offset'] for x in atoms if x['type']=='moov')<next(x['offset'] for x in atoms if x['type']=='mdat')
checks={'1440_frames':v['nb_frames']=='1440','60_fps':v['avg_frame_rate']=='60/1','1080p':(v['width'],v['height'])==(1920,1080),'duration_24':float(j['format']['duration'])==24,'h264_yuv420p_bt709':v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['color_space']=='bt709','aac_stereo_48k':a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000','full_decode_no_errors':(root/'evidence/final-decode.log').read_text()=='','true_peak_below_minus1':float(l['input_tp'])<-1,'audio_near_minus18_lufs':abs(float(l['input_i'])+18)<1,'browser_completed':browser['fullPlayback']['ended'] and browser['fullPlayback']['readyState']==4 and browser['fullPlayback']['error'] is None,'frame_step_observed':browser['frameInput']['presentedFrame']==540 and browser['nextFrame']['presentedFrame']==541,'motion_numeric_pass':motion['passed'],'local_links_pass':links['passed'],'faststart':faststart}
report={'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'video':{'width':v['width'],'height':v['height'],'fps':60,'frames':1440,'duration':24,'codec':v['codec_name'],'pixelFormat':v['pix_fmt'],'colorRange':v['color_range'],'colorSpace':v['color_space']},'audio':{'codec':a['codec_name'],'sampleRate':48000,'channels':2,'integratedLUFS':float(l['input_i']),'truePeakDBTP':float(l['input_tp']),'loudnessRangeLU':float(l['input_lra'])},'checks':checks,'passed':all(checks.values()),'notes':['Visual inspection of key frames, beat contact sheet and final encoded opening frame performed.','Browser playback and frame stepping verified in Codex in-app browser after disclosed Ego Lite access errors.','No claim of expert subjective audio audition or real network simulation.'],'publication':{'submitted':False,'publicUrl':None}}
(root/'evidence/final-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
assert report['passed']
