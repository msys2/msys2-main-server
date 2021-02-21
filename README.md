# MSYS2 Repo Server

Provides:

* nginx service for serving files (port 80 and 443)
* rsync server for serving files (port 873)
* letsencrypt integration

## Setup

* Clone.
* The storage is pointed to `/srv/msys2repo` so `/srv/msys2repo/mingw/x86_64/` should exist.
* Run `docker-compose up -d`.
