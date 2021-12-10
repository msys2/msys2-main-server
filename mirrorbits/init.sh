#!/bin/bash

set -e

# Throw out the redis db, mirrorbits gets confused easily when adding/removing mirrors,
# so always start fresh
redis-cli -h redis FLUSHALL

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

# add all mirrors
if [ -f "add_mirrors.sh" ]; then
    source add_mirrors.sh
fi

# Save redis DB to disk
redis-cli -h redis BGSAVE SCHEDULE

wait $pid