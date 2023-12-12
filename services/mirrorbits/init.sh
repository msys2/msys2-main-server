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

# Save redis DB to disk
redis-cli -h redis BGSAVE SCHEDULE

wait $pid