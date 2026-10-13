from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json, os, re, socket
root=Path(__file__).resolve().parents[1]
files={"/":(root/"review.html","text/html; charset=utf-8"),"/media/lauren-tan-session-65m-720p.mp4":(root/"media/lauren-tan-session-65m-720p.mp4","video/mp4"),"/verification/early-frame.jpg":(root/"verification/early-frame.jpg","image/jpeg")}
class Handler(BaseHTTPRequestHandler):
 def do_HEAD(self):self.serve(False)
 def do_GET(self):self.serve(True)
 def serve(self,body):
  item=files.get(self.path.split("?")[0])
  if not item or not item[0].is_file():self.send_error(404);return
  path,kind=item;size=path.stat().st_size;a=0;b=size-1;status=200
  rng=self.headers.get("Range")
  if rng:
   match=re.fullmatch(r"bytes=(\d+)-(\d*)",rng)
   if not match:self.send_error(416);return
   a=int(match[1]);b=min(int(match[2]),size-1) if match[2] else size-1;status=206
   if a>b:self.send_error(416);return
  self.send_response(status);self.send_header("Content-Type",kind);self.send_header("Content-Length",str(b-a+1));self.send_header("Accept-Ranges","bytes")
  if status==206:self.send_header("Content-Range",f"bytes {a}-{b}/{size}")
  self.end_headers()
  if body:
   try:
    with path.open("rb") as f:
     f.seek(a);left=b-a+1
     while left:
      data=f.read(min(1024*1024,left))
      if not data:break
      self.wfile.write(data);left-=len(data)
   except (BrokenPipeError,ConnectionResetError):pass
 def log_message(self,*args):pass
server=ThreadingHTTPServer(("0.0.0.0",0),Handler)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.connect(("8.8.8.8",80));ip=s.getsockname()[0];s.close()
record={"pid":os.getpid(),"port":server.server_port,"local_url":f"http://127.0.0.1:{server.server_port}/","lan_url":f"http://{ip}:{server.server_port}/","scope":"only review HTML, selected video, and poster"}
(root/"verification/review-server.json").write_text(json.dumps(record,indent=2));print(json.dumps(record),flush=True)
server.serve_forever()
