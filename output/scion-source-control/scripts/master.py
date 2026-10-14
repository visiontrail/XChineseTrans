import subprocess,json,pathlib,re
p=pathlib.Path(__file__).resolve().parents[1]
src=p/'scion-render.mp4';out=p/'scion-explained.mp4'
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(src),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
m=json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',r.stderr)[-1])
f=f"loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
r=subprocess.run(['ffmpeg','-hide_banner','-y','-i',str(src),'-af',f,'-c:v','copy','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-c:a','aac','-ar','48000','-ac','2','-b:a','192k','-movflags','+faststart',str(out)],capture_output=True,text=True,check=True)
(p/'evidence/master.json').write_text(json.dumps({'input':m,'normalization':json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',r.stderr)[-1]),'target_lufs':-16,'target_dbtp':-1.5},indent=2)+'\n')
print(out)
