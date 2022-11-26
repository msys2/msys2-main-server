FROM ubuntu:jammy

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends rsync && \
  apt-get clean autoclean && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 873

CMD ["/usr/bin/rsync", "--no-detach", "--daemon", "--config", "/etc/rsyncd.conf"]