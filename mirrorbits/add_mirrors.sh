#!/bin/bash

mirrorbits add -http=https://repo.msys2.org/ -rsync=rsync://repo.msys2.org/builds/ repo.msys2.org
mirrorbits enable repo.msys2.org

mirrorbits add -http=https://mirror.yandex.ru/mirrors/msys2/ -rsync=rsync://mirror.yandex.ru/mirrors/msys2/ mirror.yandex.ru
mirrorbits enable mirror.yandex.ru

mirrorbits add -http=https://mirror.selfnet.de/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ mirror.selfnet.de
mirrorbits enable mirror.selfnet.de

mirrorbits add -country-only -http=https://mirrors.tuna.tsinghua.edu.cn/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ mirrors.tuna.tsinghua.edu.cn
mirrorbits enable mirrors.tuna.tsinghua.edu.cn

mirrorbits add -country-only -http=https://mirrors.ustc.edu.cn/msys2/ -rsync=rsync://rsync.mirrors.ustc.edu.cn/repo/msys2/ mirrors.ustc.edu.cn
mirrorbits enable mirrors.ustc.edu.cn

mirrorbits add -http=https://ftp.acc.umu.se/mirror/msys2.org/ -rsync=rsync://ftp.acc.umu.se/mirror/msys2.org/ ftp.acc.umu.se
mirrorbits enable ftp.acc.umu.se

mirrorbits add -http=https://mirrors.dotsrc.org/msys2/ -rsync=rsync://mirrors.dotsrc.org/msys2/ mirrors.dotsrc.org
mirrorbits enable mirrors.dotsrc.org

# -continent-only so it doesn't serve users from africa
mirrorbits add -continent-only -http=https://mirror.ufro.cl/msys2/ -rsync=rsync://mirror.ufro.cl/msys2/ mirror.ufro.cl
mirrorbits enable mirror.ufro.cl

mirrorbits add -http=https://ftp.nluug.nl/pub/os/windows/msys2/builds/ -rsync=rsync://ftp.nluug.nl/msys2/builds/ ftp.nluug.nl
mirrorbits enable ftp.nluug.nl

mirrorbits add -http=https://download.nus.edu.sg/mirror/msys2/ -rsync=rsync://download.nus.edu.sg/msys2/ download.nus.edu.sg
mirrorbits enable download.nus.edu.sg

mirrorbits add -http=https://mirror.clarkson.edu/msys2/ -rsync=rsync://mirror.clarkson.edu/msys2/ mirror.clarkson.edu
mirrorbits enable mirror.clarkson.edu

mirrorbits add -http=https://ftp.osuosl.org/pub/msys2/ -rsync=rsync://rsync.osuosl.org/msys2/ ftp.osuosl.org
mirrorbits enable ftp.osuosl.org

mirrorbits add -http=https://quantum-mirror.hu/mirrors/pub/msys2/ -rsync=rsync://quantum-mirror.hu/msys2/ quantum-mirror.hu
# Seems slow
# mirrorbits enable quantum-mirror.hu

mirrorbits add -http=https://fastmirror.pp.ua/msys2/ -rsync=rsync://fastmirror.pp.ua/msys2/ fastmirror.pp.ua
# Seems slow
# mirrorbits enable fastmirror.pp.ua
