const http = require('http');
const fs = require('fs');
const path = require('path');
const port = Number(process.env.PORT || 5500);
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8'};
http.createServer((req,res)=>{
  const pathname = decodeURIComponent(new URL(req.url, `http://${req.headers.host}`).pathname);
  const files = {'/':'index.html','/index.html':'index.html','/style.css':'style.css','/script.js':'script.js'};
  const file = files[pathname];
  if (!file) {res.writeHead(404);return res.end('Not Found')}
  fs.readFile(path.join(__dirname,file),(err,data)=>{
    if(err){res.writeHead(500);return res.end('Server error')}
    res.writeHead(200,{'Content-Type':mime[path.extname(file)]});res.end(data);
  });
}).listen(port,'0.0.0.0',()=>console.log(`Front-end rodando na porta ${port}`));
