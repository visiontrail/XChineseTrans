from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import re
ROOT=Path(__file__).parent
ASSETS={'/':('review.html','text/html; charset=utf-8'),'/video.mp4':('source-clip-verified.mp4','video/mp4')}
class Handler(BaseHTTPRequestHandler):
 def serve(self,body=True):
  if self.path not in ASSETS:self.send_error(404);return
  name,mime=ASSETS[self.path]; p=ROOT/name
  if not p.exists():self.send_error(503);return
  size=p.stat().st_size; start,end=0,size-1; status=200
  r=self.headers.get('Range','')
  if r:
   m=re.fullmatch(r'bytes=(\d+)-(\d*)',r)
   if not m:self.send_error(416);return
   start=int(m[1]);end=min(int(m[2]) if m[2] else size-1,size-1)
   if start>end:self.send_error(416);return
   status=206
  self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
  if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  self.end_headers()
  if body:
   with p.open('rb') as f:
    f.seek(start); left=end-start+1
    while left:
     data=f.read(min(left,1024*1024))
     if not data:break
     try:self.wfile.write(data)
     except (BrokenPipeError,ConnectionResetError):break
     left-=len(data)
 def do_GET(self):self.serve()
 def do_HEAD(self):self.serve(False)
ThreadingHTTPServer(('0.0.0.0',8887),Handler).serve_forever()
