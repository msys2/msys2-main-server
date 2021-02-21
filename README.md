# MSYS2 Repo Server

Provides:

* nginx service for serving files (port 80 and 443)
* rsync server for serving files (port 873)
* letsencrypt integration


## Setup

* Clone.
* The storage is pointed to `/srv/msys2repo` so `/srv/msys2repo/mingw/x86_64/` should exist.
* Run `docker-compose up -d`.


## Test

```
$ rsync --list-only rsync://$SERVER/builds/
drwxr-xr-x          4,096 2020/10/07 21:36:48 .
drwxr-xr-x          4,096 2021/02/10 12:32:43 distrib
drwxr-xr-x          4,096 2015/07/22 19:03:02 mingw
drwxr-xr-x          4,096 2015/07/22 19:03:02 msys
```

```
$ curl -i --connect-to repo.msys2.org:80:$SERVER:80 http://repo.msys2.org/
HTTP/1.1 200 OK
Content-Type: text/html
Date: Sun, 21 Feb 2021 17:36:18 GMT
Server: nginx/1.19.7
Content-Length: 433

<html>
<head><title>Index of /</title></head>
<body>
<h1>Index of /</h1><hr><pre><a href="../">../</a>
<a href="distrib/">distrib/</a>                                           10-Feb-2021 11:32       -
<a href="mingw/">mingw/</a>                                             22-Jul-2015 17:03       -
<a href="msys/">msys/</a>                                              22-Jul-2015 17:03       -
</pre><hr></body>
</html>
```

```
$ curl -ki --connect-to repo.msys2.org:443:$SERVER:443 https://repo.msys2.org/
HTTP/1.1 200 OK
Content-Type: text/html
Date: Sun, 21 Feb 2021 17:36:14 GMT
Server: nginx/1.19.7
Content-Length: 433

<html>
<head><title>Index of /</title></head>
<body>
<h1>Index of /</h1><hr><pre><a href="../">../</a>
<a href="distrib/">distrib/</a>                                           10-Feb-2021 11:32       -
<a href="mingw/">mingw/</a>                                             22-Jul-2015 17:03       -
<a href="msys/">msys/</a>                                              22-Jul-2015 17:03       -
</pre><hr></body>
</html>
```
