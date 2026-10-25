#!/usr/bin/env python3
"""Preview docs/ locally the way GitHub Pages serves it: /little-owl -> little-owl.html.

    python3 serve.py [port]
"""
import http.server
import os
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS, **kwargs)

    def send_head(self):
        path = self.path.split("?")[0].rstrip("/")
        if path and "." not in os.path.basename(path) and os.path.exists(os.path.join(DOCS, path.lstrip("/") + ".html")):
            self.path = path + ".html"
        elif path and not os.path.exists(os.path.join(DOCS, path.lstrip("/"))):
            self.path = "/404.html"
        return super().send_head()


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
print(f"Previewing on http://localhost:{port}")
http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()
