# MSYS2 main server

Provides:

* nginx service for serving installers and packages (ports 80 and 443)
* rsync server for serving the same (port 873)
* daemon and http server for staging repositories
* letsencrypt integration
* packages web interface and API
* redirects from non-canonical domains


## Setup

* Clone.
* The storage is pointed to `/srv/msys2repo` so `/srv/msys2repo/mingw/x86_64/` should exist.
* Run `docker-compose up -d`.
* Assign DNS records for:
  * repo.msys2.org
  * packages.msys2.org
  * msys2.org
  * NOT www.msys2.org, that is on GitHub Pages.
  * msys2.com
  * www.msys2.com
  * msys2.net
  * www.msys2.net


## Test

Once everything is set up and running you can run

```shell
> python3 test.py
....
----------------------------------------------------------------------
Ran 4 tests in 5.909s

OK
```

... which checks if all services are up and responding properly.


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
