"""Preview the generated static site on the user's local machine."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import threading,webbrowser
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'dist/index.html').exists():raise SystemExit('Run python scripts/build.py first.')
server=ThreadingHTTPServer(('127.0.0.1',4173),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'dist')))
url='http://127.0.0.1:4173/'
print('Preview: '+url+'  (Ctrl+C to stop)',flush=True)
threading.Timer(.5,lambda:webbrowser.open(url)).start()
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
