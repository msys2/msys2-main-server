#!/bin/bash

set -e

while [ ! -f /usr/share/GeoIP/GeoLite2-ASN.mmdb ] || [ ! -f /usr/share/GeoIP/GeoLite2-ASN.mmdb ]
do
    echo "waiting for GeoIP data to be loaded"
    sleep 1
done

mirrorbits daemon --debug &
pid=$!

while ! mirrorbits list
do
  echo "waiting for server"
  sleep 1
done

# remove all mirrors
mirrorbits list -state=false | tail -n +2 | xargs --no-run-if-empty -n1 mirrorbits remove -f

# add all mirrors
if [ -f "add_mirrors.sh" ]; then
    source add_mirrors.sh
fi

REDIS_HOST=$(grep "RedisAddress" /etc/mirrorbits.conf | cut -d ':' -f 2 | xargs)
REDIS_PORT=$(grep "RedisAddress" /etc/mirrorbits.conf | cut -d ':' -f 3 | xargs)

# Save redis DB to disk
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" BGSAVE SCHEDULE

wait $pid