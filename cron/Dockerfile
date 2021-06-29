FROM ubuntu:focal

RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    busybox-static \
    && rm -rf /var/lib/apt/lists/*;

RUN mkdir -p /var/spool/cron/crontabs
RUN mkdir -p /repo-volume
RUN echo '*/5 * * * * date +%s > /repo-volume/lastsync' > /var/spool/cron/crontabs/root

ENTRYPOINT [ "tini", "--", "busybox", "crond", "-f", "-l", "1", "-L", "/dev/stdout" ]