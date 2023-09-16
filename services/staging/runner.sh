#!/bin/bash

set -eu
shopt -s nullglob

pub=/srv/msys2staging
cache=/tmp/msys2cache

init() {
    local keyname="CD (msys2-autobuild)"
    touch "${pub}/~initializing"
    chmod go-rwx ~/.gnupg/
    if ! gpg --list-secret-keys "${keyname}"
    then
        gpg --batch --passphrase "" --quick-generate-key "${keyname}" future-default sign never
    fi
    rm -rf msys2-autobuild
    git clone https://github.com/msys2/msys2-autobuild
}

update() {
    git -C msys2-autobuild pull
    pip3 install -r msys2-autobuild/requirements.txt

    mkdir -p "${cache}/"
    PYTHONPATH=msys2-autobuild python3 -m msys2_autobuild fetch-assets --noconfirm --fetch-all --delete "${cache}/"

    local staging="$(mktemp --tmpdir -d "msys2staging.$(date +"%Y-%m-%d.%H%M%S").XXXXXXXX")"
    echo "${cache}"/*/*/*.{pkg,src}.tar.{gz,xz,zst} | xargs -r cp -a -t "${staging}/"
    echo "${staging}"/*.{pkg,src}.tar.{gz,xz,zst} | xargs -rn1 gpg --detach-sign

    # __empty__ package ensures database exists even if empty
    export ZSTD_CLEVEL=19
    repo-add -q -s -v "${staging}/staging.db.tar.zst" "${staging}"/*.pkg.tar.{gz,xz,zst} "__empty__-0-1-any.pkg.tar.gz"
    repo-remove -q -s -v "${staging}/staging.db.tar.zst" __empty__
    gpg --verify "${staging}/staging.db.tar.zst"{.sig,}
    gpg --verify "${staging}/staging.db.tar.zst"{.sig,}

    # ~updating marker will be removed by rsync when it's done
    touch "${pub}/~updating"
    rsync -rtl --delete-after --delay-updates --safe-links "${staging}/" "${pub}/"
    rm -r "${staging}"
}

echo "Initializing"
init
while true
do
    echo "Creating a new staging repo"
    update || true
    echo "Waiting 15 minutes"
    sleep 15m
done
