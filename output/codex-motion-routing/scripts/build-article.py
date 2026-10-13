from pathlib import Path
import re, html
p=Path(__file__).resolve().parent.parent
lines=(p/'article.md').read_text().splitlines()
def inline(s):
 s=html.escape(s)
 s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<a href="\2">\1</a>',s)
 return s
blocks=[];paragraph=[];code=[];table=[];in_code=False
def flush():
 if paragraph:blocks.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
def flush_table():
 if not table:return
 cells=[[c.strip() for c in x.strip('|').split('|')] for x in table]
 blocks.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in cells[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in r)+'</tr>' for r in cells[2:])+'</tbody></table></div>');table.clear()
for line in lines:
 if line.startswith('```'):
  flush();flush_table()
  if in_code:blocks.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');code=[]
  in_code=not in_code;continue
 if in_code:code.append(line);continue
 if line.startswith('|'):flush();table.append(line);continue
 flush_table()
 if not line:flush();continue
 if line.startswith('# '):flush();continue
 if line.startswith('## '):flush();blocks.append('<h2>'+inline(line[3:])+'</h2>');continue
 if line.startswith('> '):flush();blocks.append('<blockquote>'+inline(line[2:])+'</blockquote>');continue
 paragraph.append(line)
flush();flush_table()
body='\n'.join(blocks)
# Add actual frame evidence in the relevant parts of the article.
body=body.replace('<h2>Give the video one job</h2>','<figure class="wide"><video controls playsinline preload="metadata" poster="frames/frame-0090.png" src="route-around-failure.mp4"></video><figcaption>A route around failure · 24 seconds · original motion and sound</figcaption></figure><h2>Give the video one job</h2>')
body=body.replace('<h2>Review the motion and the encoded file</h2>','<figure class="wide compare"><div><img src="research/first-pass/opening-low-contrast.png" alt="First render with pale text caused by the paper layer painting over the artwork"><img src="frames/frame-0090.png" alt="Corrected render with dark green text and the paper behind the artwork"></div><figcaption>Before and after correcting the texture layer. The palette values did not change.</figcaption></figure><h2>Review the motion and the encoded file</h2>')
style='''@font-face{font-family:Geist;src:url(public/Geist-Regular.woff2)}@font-face{font-family:Geist;src:url(public/Geist-Medium.woff2);font-weight:500}*{box-sizing:border-box}body{margin:0;background:#FDFBF7;color:#1A4A3A;font-family:Geist,sans-serif}nav{max-width:1120px;margin:auto;padding:30px 28px 20px;display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid #d6ddcf}a{color:#1a4a3a;text-underline-offset:4px}header{max-width:1000px;margin:68px auto 42px;padding:0 28px}.eyebrow{font-size:12px;letter-spacing:.14em;color:#80601b}h1{font-weight:500;font-size:clamp(36px,5.5vw,65px);line-height:1.1;letter-spacing:-.045em;margin:20px 0}.deck{color:#426454;font-size:19px;line-height:1.6;max-width:710px}article{max-width:790px;margin:auto;padding:0 28px 70px;font-size:17px;line-height:1.8}p{margin:0 0 22px}h2{font-size:29px;font-weight:500;line-height:1.25;letter-spacing:-.035em;margin:53px 0 23px}pre{background:#f2f1e9;padding:23px;font-size:13px;line-height:1.8;overflow-x:auto}code{font-family:ui-monospace,monospace;font-size:.88em}.table-wrap{overflow-x:auto;margin:30px 0}table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.65}td,th{padding:15px 10px;text-align:left;border-bottom:1px solid #d6ddcf;min-width:100px}th{font-weight:500;color:#80601b}blockquote{margin:30px 0;padding:8px 0 8px 23px;border-left:2px solid #80601b;color:#426454;font-size:17px}.wide{width:calc(100% + 120px);margin:40px -60px}video,img{width:100%;display:block}figcaption{font-size:12px;color:#426454;margin-top:12px;line-height:1.6}.compare>div{display:grid;grid-template-columns:1fr 1fr;gap:10px}footer{border-top:1px solid #d6ddcf;padding-top:25px;margin-top:50px;font-size:13px;display:flex;justify-content:space-between;gap:24px}@media(max-width:900px){.wide{width:100%;margin:32px 0}}@media(max-width:560px){header{margin:40px auto 30px}article{font-size:16px}.compare>div{grid-template-columns:1fr}h2{font-size:25px}.deck{font-size:17px}pre{padding:15px;font-size:11px}}'''
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>How I used Codex to make a motion video from a director brief</title><style>'+style+'</style><nav><span>LeoGuoLabs</span><a href="review.html">Film and frame viewer →</a></nav><header><p class="eyebrow">A PRACTICAL CODEX EXPERIMENT</p><h1>How I used Codex to make a motion video from a director brief</h1><p class="deck">One 24-second film, a shared timeline, original sound, and a correction that only appeared in the rendered frames.</p></header><article>'+body+'<footer><a href="route-around-failure.mp4" download>Download the film</a><a href="article.md">Article text</a><a href="prompts.md">Reusable prompts</a></footer></article></html>'
(p/'article.html').write_text(page)
print('article.html built; words:',len((p/'article.md').read_text().split()))
