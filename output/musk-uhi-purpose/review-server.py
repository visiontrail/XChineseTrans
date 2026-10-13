from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,socket
ROOT=Path(__file__).resolve().parent
ASSETS={'/':('review.html','text/html; charset=utf-8'),'/video.mp4':('media/musk-universal-high-income-original.mp4','video/mp4'),'/poster.jpg':('verification/frame-start.jpg','image/jpeg')}
class Handler(BaseHTTPRequestHandler):
 def send_asset(self,body=True):
  if self.path not in ASSETS:self.send_error(404);return
  name,mime=ASSETS[self.path];data=(ROOT/name).read_bytes();start,end=0,len(data)-1;status=200
  r=self.headers.get('Range','')
  if r.startswith('bytes='):
   a,b=r[6:].split('-',1)
   if not a:self.send_error(416);return
   start=int(a);end=min(int(b) if b else end,end);status=206
   if start>end:self.send_error(416);return
  self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
  if status==206:self.send_header('Content-Range',f'bytes {start}-{end}/{len(data)}')
  self.end_headers()
  if body:self.wfile.write(data[start:end+1])
 def do_GET(self):self.send_asset()
 def do_HEAD(self):self.send_asset(False)
server=ThreadingHTTPServer(('0.0.0.0',0),Handler)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(('1.1.1.1',80));ip=s.getsockname()[0];s.close()
meta={'port':server.server_port,'local_url':f'http://127.0.0.1:{server.server_port}/','lan_url':f'http://{ip}:{server.server_port}/'}
(ROOT/'verification/review-server.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta),flush=True)
server.serve_forever()
