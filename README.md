This is a simple docker container to do Google Play mitm and decode/log.

It creates a lot of logs (javascriopt to make request, pb for binary protobuf, and json for raw-parsed protobuf) and you probly want to use same config across runs and expose ports:


```
# Start a web-server GUI
docker run -p 8081:8081 -p 8080:8080 -v $(pwd)/mitm-config:/home/mitmproxy/.mitmproxy -v $(pwd)/out:/out -it --rm konsumer/fdfe_mitm web

# Start an interactive  TUI
docker run -p 8080:8080 -v $(pwd)/mitm-config:/home/mitmproxy/.mitmproxy -v $(pwd)/out:/out -it --rm konsumer/fdfe_mitm proxy

# just dump/log
docker run -p 8080:8080 -v $(pwd)/mitm-config:/home/mitmproxy/.mitmproxy -v $(pwd)/out:/out -it --rm konsumer/fdfe_mitm

# If you want to play around with the logging script (live-reloading):
docker run -p 8081:8081 -p 8080:8080 -v $(pwd)/mitm_google_fdfe.py:/usr/share/mitm_google_fdfe.py -v $(pwd)/mitm-config:/home/mitmproxy/.mitmproxy -v $(pwd)/out:/out -it --rm konsumer/fdfe_mitm web
```