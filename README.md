# MSYS2 Repo Server

Provides:

* nginx service for serving files (port 80 and 443)
* rsync server for serving files (port 873)
* letsencrypt integration

## Setup

* Clone this to the same level as the root repo dir (called `msys2`)
* `../msys2/mingw/x86_64` should exist
* Run `docker-compose up -d`