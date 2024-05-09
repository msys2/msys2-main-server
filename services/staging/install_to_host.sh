#!/bin/bash

set -e

docker build --tag ubuntu-pacman --target installed .
docker run --rm ubuntu-pacman tar -czf - /etc/{makepkg,pacman}.conf /var/cache/pacman/pkg /var/lib/pacman/ /usr/local/{bin,include,lib,share} | tar -xzf - -C /
apt install libarchive13 libarchive-tools libcurl4 libgpgme11 libssl3 zstd
ldconfig
