#!/bin/bash

# mirrorbits add -http=https://repo.msys2.org/ -rsync=rsync://repo.msys2.org/builds/ repo.msys2.org
# It's configured as a fallback and we have enough mirrors now, so let it focus on redirecting
# mirrorbits enable repo.msys2.org

mirrorbits add -http=https://mirror.yandex.ru/mirrors/msys2/ -rsync=rsync://mirror.yandex.ru/mirrors/msys2/ mirror.yandex.ru
mirrorbits enable mirror.yandex.ru

mirrorbits add -http=https://mirror.selfnet.de/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ mirror.selfnet.de
mirrorbits enable mirror.selfnet.de

mirrorbits add -http=https://mirrors.tuna.tsinghua.edu.cn/msys2/ -rsync=rsync://mirrors.tuna.tsinghua.edu.cn/msys2/ mirrors.tuna.tsinghua.edu.cn
mirrorbits enable mirrors.tuna.tsinghua.edu.cn

mirrorbits add -http=https://mirrors.ustc.edu.cn/msys2/ -rsync=rsync://rsync.mirrors.ustc.edu.cn/repo/msys2/ mirrors.ustc.edu.cn
mirrorbits enable mirrors.ustc.edu.cn

mirrorbits add -http=https://mirror.nju.edu.cn/msys2/ -rsync=rsync://mirror.nju.edu.cn/msys2/ mirror.nju.edu.cn
mirrorbits enable mirror.nju.edu.cn

mirrorbits add -http=https://mirrors.bfsu.edu.cn/msys2/ -rsync=rsync://mirrors.bfsu.edu.cn/msys2/ mirrors.bfsu.edu.cn
mirrorbits enable mirrors.bfsu.edu.cn

mirrorbits add -http=https://mirror.accum.se/mirror/msys2.org/ -rsync=rsync://mirror.accum.se/mirror/msys2.org/ mirror.accum.se
mirrorbits enable mirror.accum.se

mirrorbits add -http=https://mirrors.dotsrc.org/msys2/ -rsync=rsync://mirrors.dotsrc.org/msys2/ mirrors.dotsrc.org
mirrorbits enable mirrors.dotsrc.org

mirrorbits add -http=https://ftp.nluug.nl/pub/os/windows/msys2/builds/ -rsync=rsync://ftp.nluug.nl/msys2/builds/ ftp.nluug.nl
mirrorbits enable ftp.nluug.nl

mirrorbits add -http=https://ftp-chi.osuosl.org/pub/msys2/ -rsync=rsync://ftp-chi.osuosl.org/msys2/ ftp-chi.osuosl.org
mirrorbits enable ftp-chi.osuosl.org

mirrorbits add -http=https://ftp-nyc.osuosl.org/pub/msys2/ -rsync=rsync://ftp-nyc.osuosl.org/msys2/ ftp-nyc.osuosl.org
mirrorbits enable ftp-nyc.osuosl.org

mirrorbits add -http=https://ftp-osl.osuosl.org/pub/msys2/ -rsync=rsync://ftp-osl.osuosl.org/msys2/ ftp-osl.osuosl.org
mirrorbits enable ftp-osl.osuosl.org

mirrorbits add -http=https://mirror.internet.asn.au/pub/msys2/ -rsync=rsync://mirror.internet.asn.au/msys2/ mirror.internet.asn.au
mirrorbits enable mirror.internet.asn.au

mirrorbits add -http=https://mirror.umd.edu/msys2/ -rsync=rsync://mirror.umd.edu/msys2/ mirror.umd.edu
# currently flaky
#mirrorbits enable mirror.umd.edu

mirrorbits add -http=https://mirror.clarkson.edu/msys2/ -rsync=rsync://mirror.clarkson.edu/msys2/ mirror.clarkson.edu
mirrorbits enable mirror.clarkson.edu

mirrorbits add -http=https://mirror.archlinux.tw/MSYS2/ -rsync=rsync://mirror.archlinux.tw/msys2/ mirror.archlinux.tw
mirrorbits enable mirror.archlinux.tw

mirrorbits add -http=https://quantum-mirror.hu/mirrors/pub/msys2/ -rsync=rsync://quantum-mirror.hu/msys2/ quantum-mirror.hu
mirrorbits enable quantum-mirror.hu

mirrorbits add -http=https://distrohub.kyiv.ua/msys2/ -rsync=rsync://distrohub.kyiv.ua/msys2/ distrohub.kyiv.ua
mirrorbits enable distrohub.kyiv.ua
