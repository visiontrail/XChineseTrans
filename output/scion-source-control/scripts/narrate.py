import asyncio, json, pathlib, subprocess, math, re, html
import edge_tts
P=pathlib.Path(__file__).resolve().parents[1]
VOICE='en-US-AndrewMultilingualNeural'
async def main():
 script=json.loads((P/'script.json').read_text()); out=[]; caps=[]; cursor=0
 (P/'public/voice').mkdir(exist_ok=True)
 for i,s in enumerate(script):
  mp3=P/f'public/voice/{i:02d}.mp3'; meta=P/f'public/voice/{i:02d}.json'
  if not mp3.exists() or not meta.exists():
   chunks=[]
   with mp3.open('wb') as f:
    async for c in edge_tts.Communicate(' '.join(s['lines']),VOICE,rate='-3%',boundary='WordBoundary').stream():
     if c['type']=='audio':f.write(c['data'])
     elif c['type']=='WordBoundary': chunks.append(c)
   meta.write_text(json.dumps(chunks,indent=2))
  chunks=json.loads(meta.read_text()); dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(mp3)]))
  n=math.ceil((dur+(3.25 if i==len(script)-1 else 2.0))*30); shot=dict(s,start=cursor,end=cursor+n,voiceStart=cursor+18,voiceFrames=math.ceil(dur*30),voice=f'voice/{i:02d}.mp3')
  out.append(shot)
  source=' '.join(s['lines']); pos=0; sentence=[]
  def emit(words):
   length=words[-1]['charEnd']-words[0]['charStart']; parts=max(1,math.ceil(length/94)); count=len(words)
   for k in range(parts):
    first=round(k*count/parts); last=round((k+1)*count/parts)-1
    a,b=words[first],words[last]
    start=cursor+18+round(a['offset']/1e7*30)
    end=cursor+18+round((b['offset']+b['duration'])/1e7*30)+2
    caps.append(dict(start=start,end=end,text=source[a['charStart']:b['charEnd']]))
  for j,c in enumerate(chunks):
   word=html.unescape(c['text']); at=source.casefold().find(word.casefold(),pos)
   if at<0: raise ValueError(f"Unmatched word {word!r} in {s['id']}")
   endchar=at+len(word)
   while endchar<len(source) and source[endchar] in ',.!?:;': endchar+=1
   sentence.append(dict(c,charStart=at,charEnd=endchar));pos=endchar
   if source[at:endchar].endswith(('.', '?', '!')) or j==len(chunks)-1:
    emit(sentence);sentence=[]
  cursor+=n
  print(s['id'],round(dur,2),'seconds',flush=True)
 for a,b in zip(caps,caps[1:]): a['end']=min(a['end'],b['start'])
 timeline=dict(fps=30,width=1920,height=1080,duration_frames=cursor,shots=out,captions=caps,events=[dict(id=s['id']+'-reveal',frame=s['start']+15) for s in out])
 cue_words={
 'bottleneck':{'growth':'September','downstream':'More'},
 'git':{'offline':'offline'},
 'partial':{'shallow':'Shallow','partial':'Partial','sparse':'Sparse'},
 'contract':{'server':'server'},
 'demand':{'locally':'locally','upstream':'upstream','appears':'appears','reuse':'reuse'},
 'api':{'changeset':'changesets','content':'content'},
 'cache':{'reuse':'Imagine'},
 'results':{'ci':'twenty'},
 'tradeoff':{'questions':'For'},
 'close':{'lesson':'Then'}
 }
 for i,shot in enumerate(out):
  chunks=json.loads((P/f'public/voice/{i:02d}.json').read_text());shot['cues']={}
  for name,word in cue_words[shot['id']].items():
   hits=[c for c in chunks if c['text'].casefold().strip('.,?!')==word.casefold()]
   hit=(hits[-1] if shot['id']=='tradeoff' else hits[0]) if hits else None
   if not hit:
    hit=next((c for c in chunks if c['text'].casefold().startswith(word.casefold())),None)
   if not hit:raise ValueError(f"Missing cue {shot['id']} {word}")
   frame=shot['voiceStart']+round(hit['offset']/1e7*30)
   shot['cues'][name]=frame;timeline['events'].append(dict(id=shot['id']+'-'+name,frame=frame))
 (P/'public/timeline.json').write_text(json.dumps(timeline,indent=2))
 def ts(f):
  ms=round(f/30*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);ss,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{ss:02},{ms:03}'
 (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n{c["text"]}' for i,c in enumerate(caps))+'\n')
 (P/'evidence/voice-provenance.json').write_text(json.dumps(dict(provider='Microsoft Edge speech service via edge-tts',voice=VOICE,rate='-3%',edge_tts=edge_tts.__version__,text='narration.txt',cloned_voice=False),indent=2))
 print('Total:',cursor/30,'seconds',flush=True)
asyncio.run(main())
