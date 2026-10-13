import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(), port=Number(process.env.PORT||8743);
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.json':'application/json','.css':'text/css','.mp4':'video/mp4','.wav':'audio/wav','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2','.md':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8'};
http.createServer((req,res)=>{
 let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
 if(p==='/')p='/review.html';
 const file=path.resolve(root,'.'+p);
 if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||fs.statSync(file).isDirectory()){res.writeHead(404);res.end('Not found');return;}
 const size=fs.statSync(file).size,range=req.headers.range;
 const headers={'Content-Type':mime[path.extname(file)]||'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
 if(range){
  const m=/bytes=(\d+)-(\d*)/.exec(range);if(!m){res.writeHead(416);res.end();return;}
  const start=Number(m[1]),end=Math.min(size-1,m[2]?Number(m[2]):size-1);
  if(start>=size||end<start){res.writeHead(416,{'Content-Range':`bytes */${size}`});res.end();return;}
  res.writeHead(206,{...headers,'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});fs.createReadStream(file,{start,end}).pipe(res);
 }else{res.writeHead(200,{...headers,'Content-Length':size});fs.createReadStream(file).pipe(res);}
}).listen(port,'127.0.0.1',()=>console.log(`Review: http://127.0.0.1:${port}/review.html`));
