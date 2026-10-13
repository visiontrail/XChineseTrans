from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).parent
ASSETS={"/":("review.html","text/html; charset=utf-8"),"/video.mp4":("media/source-video.mp4","video/mp4"),"/poster.jpg":("poster.jpg","image/jpeg")}
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path not in ASSETS: self.send_error(404); return
  name,mime=ASSETS[self.path]; data=(ROOT/name).read_bytes(); start,end=0,len(data)-1; status=200
  r=self.headers.get("Range","")
  if r.startswith("bytes="):
   a,b=r[6:].split("-",1); start=int(a or 0); end=min(int(b) if b else end,end); status=206
  self.send_response(status); self.send_header("Content-Type",mime); self.send_header("Accept-Ranges","bytes"); self.send_header("Content-Length",str(end-start+1))
  if status==206:self.send_header("Content-Range",f"bytes {start}-{end}/{len(data)}")
  self.end_headers(); self.wfile.write(data[start:end+1])
ThreadingHTTPServer(("0.0.0.0",8889),Handler).serve_forever()
