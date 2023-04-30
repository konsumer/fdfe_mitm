#!/bin/bash

PROGRAM='mitmdump'

if [ "${1}" == "web" ];then
  PROGRAM='mitmweb --web-host 0.0.0.0 --showhost'
fi

if [ "${1}" == "proxy" ];then
  PROGRAM='mitmproxy'
fi

shift
exec $PROGRAM -s /usr/share/mitm_google_fdfe.py $*
