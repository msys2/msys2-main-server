# MSYS2 main server

Provides:

* nginx service for serving installers and packages (ports 80 and 443)
* rsync server for serving the same (port 873)
* daemon and http server for staging repositories
* letsencrypt integration
* packages web interface and API
* redirects from non-canonical domains
* network statistics
* instant messaging bridge between Discord and Gitter / OFTC IRC


## Setup

* Clone.
* The storage is pointed to `/srv/msys2repo` so `/srv/msys2repo/mingw/x86_64/` should exist.
* Run `docker-compose up -d`.
* Assign DNS records for:
  * repo.msys2.org
  * packages.msys2.org
  * mirror.msys2.org
  * autobuildcontroller.msys2.org
  * msys2.org
  * NOT www.msys2.org, that is on GitHub Pages.
  * msys2.com
  * www.msys2.com
  * msys2.net
  * www.msys2.net
  * mingw-w64.net
  * www.mingw-w64.net
  * mingw-w64.org
  * NOT www.mingw-w64.org, that is on GitHub Pages.


## Test

Once everything is set up and running you can run `python3 -m unittest tests/test_server.py` which checks if all services are up and responding properly.


## Staging repositories

Add to `/etc/pacman.conf` above the official repositories like this:

```ini
[staging]
Server = https://repo.msys2.org/staging/
SigLevel = Never

[mingw32]
Include = /etc/pacman.d/mirrorlist.mingw32

[mingw64]
Include = /etc/pacman.d/mirrorlist.mingw64

[msys]
Include = /etc/pacman.d/mirrorlist.msys
```

## Local Development

There is a docker-compose variant in docker-compose.dev.yml that only uses HTTP and contains
a limited set of services for local testing.

It provides the following services:

* http://localhost:8080 - the traefik dashboard
* http://repo.localhost:9090/
* http://repo.localhost:9090/staging/
* http://mirror.localhost:9090/
* http://packages.localhost
* rsync://localhost/builds

Run it with `docker-compose -f docker-compose.dev.yml ...`. For example
`docker-compose -f docker-compose.dev.yml run repo` and then access
http://repo.localhost:9090/
