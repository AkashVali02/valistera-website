"""Local QA server with byte ranges, matching seekable static-media hosting."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os, re
class Handler(SimpleHTTPRequestHandler):
 def send_head(self):
  self.remaining=None
  path=self.translate_path(self.path)
  value=self.headers.get('Range')
  if not value or not os.path.isfile(path):return super().send_head()
  size=os.path.getsize(path);match=re.fullmatch(r'bytes=(\d*)-(\d*)',value)
  if not match:return super().send_head()
  start,end=match.groups()
  if not start:start=max(0,size-int(end or 0));end=size-1
  else:start=int(start);end=min(int(end) if end else size-1,size-1)
  if start>=size or end<start:
   self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.end_headers();return None
  f=open(path,'rb');f.seek(start);self.remaining=end-start+1
  self.send_response(206);self.send_header('Content-Type',self.guess_type(path));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(self.remaining));self.end_headers();return f
 def end_headers(self):
  self.send_header('Accept-Ranges','bytes');super().end_headers()
 def copyfile(self,source,outputfile):
  if self.remaining is None:return super().copyfile(source,outputfile)
  while self.remaining:
   b=source.read(min(self.remaining,65536))
   if not b:break
   outputfile.write(b);self.remaining-=len(b)
ThreadingHTTPServer(('127.0.0.1',8092),Handler).serve_forever()
