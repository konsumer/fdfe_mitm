FROM  mitmproxy/mitmproxy

COPY mitm_google_fdfe.py /usr/share/mitm_google_fdfe.py
COPY endtrypoint.sh /usr/bin/endtrypoint.sh

RUN chmod 755 /usr/bin/endtrypoint.sh

ENTRYPOINT ["/usr/bin/endtrypoint.sh"]