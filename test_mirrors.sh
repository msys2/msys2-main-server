#!/bin/bash
# Simple script for manual testing of mirrors
# TODO: automate this and run in CI

set -e

mirrors="$(cat services/mirrorbits/add_mirrors.sh | grep -v '^\s*$\|^\s*\#' | grep -Eo '(http|https)://[a-zA-Z0-9./?=_%:-]*')"

for mirror in $mirrors
do
    echo "$mirror"
    # re tls-max 1.2: https://github.com/msys2/msys2.github.io/issues/204
    curl --max-time 10 --retry 3 --output /dev/null --silent --show-error --fail --tls-max 1.2 --location "$mirror"/lastsync || echo "failed"
done
