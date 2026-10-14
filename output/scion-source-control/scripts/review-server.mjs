import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(),port=Number(process.env.PORT||8756),host=process.env.HOST||'127.0.0.1';
const files=new Set(['/review.html','/scion-explained.mp4','/poster.jpg','/captions.srt','/narration.txt','/source/reference-en.mp4','/source/reference-zh.mp4','/public/Geist-Regular.woff2','/public/Geist-SemiBold.woff2']);
const types={'.html':'text/html; charset=utf-8','.mp4':'video/mp4','.jpg':'image/jpeg','.woff2':'font/woff2','.srt':'text/plain; charset=utf-8','.txt':'text/plain; charset=utf-8'};
http.createServer((req,res)=>{
 if(!['GET','HEAD'].includes(req.method)){res.writeHead(405);res.end();return;}
 let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(pathname==='/')pathname='/review.html';
 if(!files.has(pathname)){res.writeHead(404);res.end();return;}
 const file=path.resolve(root,'.'+pathname);if(!fs.existsSync(file)){res.writeHead(404);res.end();return;}
 const size=fs.statSync(file).size;let start=0,end=size-1,status=200;
 const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
 if(req.headers.range){const m=/^bytes=(\d+)-(\d*)$/.exec(req.headers.range);if(!m){res.writeHead(416);res.end();return;}
 start=Number(m[1]);end=m[2]?Math.min(size-1,Number(m[2])):size-1;if(start>=size||end<start){res.writeHead(416,{'Content-Range':`bytes */${size}`});res.end();return;}
 status=206;headers['Content-Range']=`bytes ${start}-${end}/${size}`;}
 headers['Content-Length']=end-start+1;res.writeHead(status,headers);if(req.method==='HEAD'){res.end();return;}fs.createReadStream(file,{start,end}).pipe(res);
}).listen(port,host,()=>console.log(`Review http://${host}:${port}/review.html`));
