#!/bin/bash

set -eu
shopt -s nullglob

pub=/srv/msys2staging
empty=__empty__-0-1-any.pkg.tar.gz

init() {
    touch "${pub}/~initializing"
    chmod go-rwx .gnupg/
    if ! gpg --list-secret-keys "CD (msys2-autobuild)"
    then
        gpg --batch --passphrase "" --quick-generate-key "CD (msys2-autobuild)" future-default sign never
    fi
    git clone https://github.com/msys2/msys2-autobuild
}

update() {
    git -C msys2-autobuild pull
    pip3 install -r msys2-autobuild/requirements.txt
    staging="$(mktemp --tmpdir -d "msys2staging.$(date +"%Y-%m-%d.%H%M%S").XXXXXXXX")"
    mkdir -p "${staging}"/{mingw,msys}/{sources,i686,x86_64}/
    python3 msys2-autobuild/autobuild.py fetch-assets --fetch-all "${staging}/"
    for pkg in "${staging}"/*/*/*.{pkg,src}.tar.{gz,xz,zst}
    do
        gpg --detach-sign "${pkg}"
    done
    repo-add -q -s -v "${staging}/mingw/x86_64/mingw64.db.tar.gz" "${staging}/mingw/x86_64"/*.pkg.tar.{gz,xz,zst} "${empty}"
    repo-remove -q -s -v "${staging}/mingw/x86_64/mingw64.db.tar.gz" __empty__
    repo-add -q -s -v "${staging}/mingw/i686/mingw32.db.tar.gz" "${staging}/mingw/i686"/*.pkg.tar.{gz,xz,zst} "${empty}"
    repo-remove -q -s -v "${staging}/mingw/i686/mingw32.db.tar.gz" __empty__
    repo-add -q -s -v "${staging}/msys/x86_64/msys.db.tar.gz" "${staging}/msys/x86_64"/*.pkg.tar.{gz,xz,zst} "${empty}"
    repo-remove -q -s -v "${staging}/msys/x86_64/msys.db.tar.gz" __empty__
    repo-add -q -s -v "${staging}/msys/i686/msys.db.tar.gz" "${staging}/msys/i686"/*.pkg.tar.{gz,xz,zst} "${empty}"
    repo-remove -q -s -v "${staging}/msys/i686/msys.db.tar.gz" __empty__
    touch "${pub}/~updating"
    rsync -rtl --delete-after --delay-updates --safe-links "${staging}/" "${pub}/"
}

echo "Initializing"
init
while true
do
    echo "Creating a new staging repo"
    update || true
    echo "Waiting 30 minutes"
    sleep 30m
done
