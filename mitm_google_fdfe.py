"""
mitm addon that will log tokens and fdfe requests

docker run --rm -it -v $(pwd)/google_fdfe.py:/google_fdfe.py -v $(pwd)/out:/out -v $(pwd)/config:/home/mitmproxy/.mitmproxy -p 8080:8080 -p 8081:8081 mitmproxy/mitmproxy mitmweb --web-host 0.0.0.0 -s /google_fdfe.py
"""

outDir = "/out"

import time
import json
import logging

def getHeaders(request):
  headers = {}
  for k,v in request.headers.items():
    headers[k] = v
  return headers


def response(flow):
  if flow.request.path.startswith("/auth"):
    headers = getHeaders(flow.request)
    op = "auth"
    fname = time.strftime(f"%Y-%m-%d_%H-%M-%S_{op}")
    
    logging.info(f"Saved {fname}.mjs in {outDir}")
    body = flow.response.get_content()
    auth = {}
    for line in body.split("\n"):
      k,v = line.split("=")
      auth[k] = v

    url = flow.request.scheme + "://" + flow.request.pretty_host + flow.request.path

    jf = open(f"{outDir}/{fname}.js", "w")
    jf.write("// headers that were sent\nexport const headers = " + json.dumps(headers, indent = 2) + "\n\n")
    jf.write("// body that was sent\nexport const body = " +  json.dumps(hflow.request.get_text()) + "\n")
    jf.write("// AUTH call\nexport const request = () => fetch('" + url + "', { method: '" + flow.request.method + "', headers, body })\n\n")
    jf.write("export default request\n")
    jf.close()

    jb = open(f"{outDir}/{fname}.json", "wb")
    jb.write(json.dumps(auth, indent = 2))
    jb.close()


  if flow.request.path.startswith("/fdfe"):
    headers = getHeaders(flow.request)
    op = flow.request.path.split('?')[0].replace("/fdfe/", "").replace("'", "\\'")
    fname = time.strftime(f"%Y-%m-%d_%H-%M-%S_{op}")

    logging.info(f"Saved {fname}.mjs and {fname}.pb in {outDir}")

    body = flow.response.get_content()
    url = flow.request.scheme + "://" + flow.request.pretty_host + flow.request.path

    jf = open(f"{outDir}/{fname}.js", "w")
    jf.write("// headers that were sent\nexport const headers = " + json.dumps(headers, indent = 2) + "\n\n")
    jf.write("// FDFE call\nexport const request = () => fetch('" + url + "', { headers })\n\n")
    jf.write("export default request\n")
    jf.close()

    jb = open(f"{outDir}/{fname}.pb", "wb")
    jb.write(body)
    jb.close()