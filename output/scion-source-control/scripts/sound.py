import wave,math,struct,pathlib
p=pathlib.Path(__file__).resolve().parents[1]/'public/transition.wav'
rate=48000;duration=.32
with wave.open(str(p),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
 for i in range(round(rate*duration)):
  t=i/rate;env=min(1,t/.008)*math.exp(-t*17)*(1-t/duration)
  n=.12*env*(math.sin(2*math.pi*660*t)+.35*math.sin(2*math.pi*990*t))
  f.writeframesraw(struct.pack('<h',round(32767*n)))
print(p)
