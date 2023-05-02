FROM  mitmproxy/mitmproxy

COPY mitm_google_fdfe.py /usr/share/mitm_google_fdfe.py
COPY entrypoint.sh /usr/bin/entrypoint.sh

RUN chmod 755 /usr/bin/entrypoint.sh

ENTRYPOINT ["/usr/bin/entrypoint.sh"]