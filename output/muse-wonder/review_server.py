from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import re, mimetypes

ROOT = Path(__file__).resolve().parent
FILES = {'/': 'review.html', '/review.html': 'review.html', '/meta-official-full.mp4': 'meta-official-full.mp4', '/video-preview.jpg': 'video-preview.jpg'}

class Handler(BaseHTTPRequestHandler):
    def respond(self, body):
        name = FILES.get(self.path.split('?', 1)[0])
        if name is None or not (ROOT / name).is_file():
            self.send_error(404)
            return
        file = ROOT / name
        size = file.stat().st_size
        start, end, status = 0, size - 1, 200
        value = self.headers.get('Range')
        if value:
            match = re.fullmatch(r'bytes=(\d+)-(\d*)', value)
            if not match:
                self.send_error(416)
                return
            start = int(match[1])
            end = min(int(match[2]) if match[2] else size - 1, size - 1)
            if start > end:
                self.send_error(416)
                return
            status = 206
        self.send_response(status)
        self.send_header('Content-Type', mimetypes.guess_type(name)[0] or 'application/octet-stream')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        if status == 206:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.end_headers()
        if body:
            with file.open('rb') as stream:
                stream.seek(start)
                remaining = end - start + 1
                try:
                    while remaining:
                        data = stream.read(min(65536, remaining))
                        self.wfile.write(data)
                        remaining -= len(data)
                except (BrokenPipeError, ConnectionResetError):
                    pass
    def do_GET(self):
        self.respond(True)
    def do_HEAD(self):
        self.respond(False)

print('Review available on port 8768', flush=True)
ThreadingHTTPServer(('0.0.0.0', 8768), Handler).serve_forever()
