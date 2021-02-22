# MSYS2 main server

Provides:

* nginx service for serving installers and packages (ports 80 and 443)
* rsync server for serving the same (port 873)
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

```
$ curl -i --connect-to packages.msys2.org:80:$SERVER:80 http://packages.msys2.org/
???
```

```
$ curl -ki --connect-to packages.msys2.org:443:$SERVER:443 https://packages.msys2.org/
???
```

```
$ curl -i --connect-to msys2.org:80:$SERVER:80 http://msys2.org
HTTP/1.1 302 Found
Location: http://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to msys2.org:443:$SERVER:443 https://msys2.org
HTTP/1.1 302 Found
Location: https://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -i --connect-to msys2.com:80:$SERVER:80 http://msys2.com
HTTP/1.1 302 Found
Location: http://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to msys2.com:443:$SERVER:443 https://msys2.com
HTTP/1.1 302 Found
Location: https://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -i --connect-to www.msys2.com:80:$SERVER:80 http://www.msys2.com
HTTP/1.1 302 Found
Location: http://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to www.msys2.com:443:$SERVER:443 https://www.msys2.com
HTTP/1.1 302 Found
Location: https://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -i --connect-to msys2.net:80:$SERVER:80 http://msys2.net
HTTP/1.1 302 Found
Location: http://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to msys2.net:443:$SERVER:443 https://msys2.net
HTTP/1.1 302 Found
Location: https://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -i --connect-to www.msys2.net:80:$SERVER:80 http://www.msys2.net
HTTP/1.1 302 Found
Location: http://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to www.msys2.net:443:$SERVER:443 https://www.msys2.net
HTTP/1.1 302 Found
Location: https://www.msys2.org/
Date: Mon, 22 Feb 2021 08:40:12 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```
