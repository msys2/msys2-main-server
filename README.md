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
HTTP/2 200
content-type: text/html
date: Mon, 22 Feb 2021 09:12:44 GMT
server: nginx/1.19.7
content-length: 135

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
HTTP/1.1 302 Found
Location: https://packages.msys2.org/
Date: Mon, 22 Feb 2021 09:13:17 GMT
Content-Length: 5
Content-Type: text/plain; charset=utf-8

Found
```

```
$ curl -ki --connect-to packages.msys2.org:443:$SERVER:443 https://packages.msys2.org/api/
HTTP/2 200
content-type: text/html; charset=utf-8
date: Mon, 22 Feb 2021 09:14:40 GMT
server: uvicorn
content-length: 983


    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css">
    <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
    <title>MSYS2 Packages API - Swagger UI</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({
        url: '/api/openapi.json',
    oauth2RedirectUrl: window.location.origin + '/api/docs/oauth2-redirect',
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true
    })
    </script>
    </body>
    </html>
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
HTTP/2 302
location: https://www.msys2.org/
content-type: text/plain; charset=utf-8
content-length: 5
date: Mon, 22 Feb 2021 09:15:28 GMT

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
HTTP/2 302
location: https://www.msys2.org/
content-type: text/plain; charset=utf-8
content-length: 5
date: Mon, 22 Feb 2021 09:16:27 GMT

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
HTTP/2 302
location: https://www.msys2.org/
content-type: text/plain; charset=utf-8
content-length: 5
date: Mon, 22 Feb 2021 09:17:43 GMT

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
HTTP/2 302
location: https://www.msys2.org/
content-type: text/plain; charset=utf-8
content-length: 5
date: Mon, 22 Feb 2021 09:18:13 GMT

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
HTTP/2 302
location: https://www.msys2.org/
content-type: text/plain; charset=utf-8
content-length: 5
date: Mon, 22 Feb 2021 09:18:39 GMT

Found
```
