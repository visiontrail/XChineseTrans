from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from html import escape
import re,json
ROOT=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_HEAD(self):self.serve(True)
 def do_GET(self):self.serve(False)
 def serve(self,head):
  path=self.path.split('?')[0]
  if path=='/':
   text=(ROOT/'post-en.txt').read_text().strip()
   paragraphs=''.join('<p>'+escape(t)+'</p>' for t in text.split('\n\n'))
   b=('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LeoGuoLabs · Post preview</title><style>body{margin:0;background:#FDFBF7;color:#1A4A3A;font:18px/1.6 system-ui,sans-serif}main{max-width:820px;margin:auto;padding:32px 22px 48px}h1{font-size:24px;font-weight:600;margin:0 0 4px}small{color:#426454}video{display:block;width:100%;margin:24px 0;background:#111}article{max-width:720px}p{margin:0 0 18px}footer{border-top:1px solid #D4AF37;margin-top:30px;padding-top:16px;font-size:14px}</style><main><h1>@LeoGuoLabs · Post preview</h1><small>Standalone post · English source video · 2:35</small><video controls playsinline preload="metadata" src="/video.mp4"></video><article>'''+paragraphs+'''</article><footer>待最终确认，尚未发布。</footer></main></html>''').encode()
   self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers()
   if not head:self.wfile.write(b)
   return
  if path!='/video.mp4':self.send_error(404);return
  f=ROOT/'media/upload-video.mp4'
  if not f.exists():self.send_error(503,'Video preparation in progress');return
  total=f.stat().st_size;start=0;end=total-1;status=200
  if rng:=self.headers.get('Range'):
   m=re.fullmatch(r'bytes=(\d+)-(\d*)',rng)
   if not m:self.send_error(416);return
   start=int(m[1]);end=min(end,int(m[2]) if m[2] else end);status=206
   if start>end:self.send_error(416);return
  self.send_response(status);self.send_header('Content-Type','video/mp4');self.send_header('Content-Length',str(end-start+1));self.send_header('Accept-Ranges','bytes')
  if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{total}')
  self.end_headers()
  if head:return
  try:
   with f.open('rb') as source:
    source.seek(start);remaining=end-start+1
    while remaining:
     b=source.read(min(1024*1024,remaining));self.wfile.write(b);remaining-=len(b)
  except (BrokenPipeError,ConnectionResetError):pass
server=ThreadingHTTPServer(('0.0.0.0',0),Handler)
(ROOT/'research/review-server.json').write_text(json.dumps({'port':server.server_port,'lan_ip':'172.16.10.59','url':f'http://172.16.10.59:{server.server_port}/'},indent=2))
print(f'REVIEW_URL=http://172.16.10.59:{server.server_port}/',flush=True)
server.serve_forever()
