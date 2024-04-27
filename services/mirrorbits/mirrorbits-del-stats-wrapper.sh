#!/bin/bash

REDIS_HOST=$(grep "RedisAddress" /etc/mirrorbits.conf | cut -d ':' -f 2 | xargs)
REDIS_PORT=$(grep "RedisAddress" /etc/mirrorbits.conf | cut -d ':' -f 3 | xargs)

/usr/bin/contrib/mirrorbits-del-stats "$@" -h "$REDIS_HOST" -p "$REDIS_PORT"
