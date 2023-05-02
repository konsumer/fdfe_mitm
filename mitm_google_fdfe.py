"""
mitm addon that will log tokens and fdfe requests

docker run --rm -it -v $(pwd)/google_fdfe.py:/google_fdfe.py -v $(pwd)/out:/out -v $(pwd)/config:/home/mitmproxy/.mitmproxy -p 8080:8080 -p 8081:8081 mitmproxy/mitmproxy mitmweb --web-host 0.0.0.0 -s /google_fdfe.py
"""

outDir = "/out"

import time
import json
import logging
import urllib.parse

# get headers object from request
def getHeaders(request):
  headers = {}
  for k,v in request.headers.items():
    headers[k] = v
  return headers

# handle all responses
def response(flow):
  if flow.request.path.startswith("/auth"):
    url = flow.request.scheme + "://" + flow.request.pretty_host + flow.request.path
    outS = flow.request.get_text()
    if outS:
      out = urllib.parse.parse_qs(outS)
      service = out["service"]

      if service and service[0] == 'oauth2:https://www.googleapis.com/auth/googleplay':
        op = "auth"
        fname = time.strftime(f"%Y-%m-%d_%H-%M-%S_{op}")
        auth_refresh = {}
        auth_refresh["email"] = out["Email"][0]
        auth_refresh["token"] = out["Token"][0]
        auth_refresh["gsfid"] = out["androidId"][0]
        auth_refresh["language"] = out["lang"][0]
        auth_refresh["country"] = out["device_country"][0]
        auth_refresh["google_play_services_version"] = out["google_play_services_version"][0]
        auth_refresh["sdk_version"] = out["sdk_version"][0]
        auth_refresh["signature"] = out["client_sig"][0]

        jr = open(f"{outDir}/{fname}-refresh.json", "w")
        jr.write(json.dumps(auth_refresh, indent = 2))
        jr.close()

        params = {}
        for k in out:
          params[k] = out[k][0]
       
        headers = getHeaders(flow.request)
        jf = open(f"{outDir}/{fname}.js", "w")
        jf.write("// headers that were sent\nexport const headers = " + json.dumps(headers, indent = 2) + "\n\n")
        jf.write("// body that was sent\nexport const params = " + json.dumps(params, indent = 2) + "\n\n")
        jf.write("// AUTH call\nexport const request = () => fetch('" + url + "', { method: 'POST', body: new URLSearchParams(params), headers })\n\n")
        jf.write("export default request\n")
        jf.close()

        body = flow.response.get_text()

        if body:
          jo = open(f"{outDir}/{fname}-out.txt", "w")
          jo.write(body)
          jo.close()

          bodyD = {}
          for line in body.split("\n"):
            k,v = line.split("=")
            bodyD[k]=v

          auth_session = {}
          auth_session["email"] = auth_refresh["email"]
          auth_session["gsfid"] = auth_refresh["gsfid"]
          auth_session["language"] = auth_refresh["language"]
          auth_session["country"] = auth_refresh["country"]
          auth_session["google_play_services_version"] = auth_refresh["google_play_services_version"]
          auth_session["sdk_version"] = auth_refresh["sdk_version"]
          auth_session["token"] = bodyD["Auth"]
          auth_session["issueAdvice"] = bodyD["issueAdvice"]
          auth_session["expiration"] = bodyD["Expiry"]
          auth_session["expirationDuration"] = bodyD["ExpiresInDurationSec"]
          auth_session["storeConsentRemotely"] = bodyD["storeConsentRemotely"]
          auth_session["isTokenSnowballed"] = bodyD["isTokenSnowballed"]


          js = open(f"{outDir}/{fname}-session.json", "w")
          js.write(json.dumps(auth_session, indent = 2))
          js.close()


      else:
        logging.info(f"Saw non-store auth: {service}")


  if flow.request.path.startswith("/fdfe"):
    headers = getHeaders(flow.request)
    op = flow.request.path.split('?')[0].replace("/fdfe/", "").replace("'", "\\'").replace('/', '-')
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