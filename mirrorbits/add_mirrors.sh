#!/bin/bash

mirrorbits add -http=https://repo.msys2.org/ -rsync=rsync://repo.msys2.org/builds/ msys2.org
mirrorbits enable msys2.org

mirrorbits add -http=https://mirror.yandex.ru/mirrors/msys2/ -rsync=rsync://mirror.yandex.ru/mirrors/msys2/ yandex.ru
mirrorbits enable yandex.ru

mirrorbits add -http=https://mirror.selfnet.de/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ selfnet.de
mirrorbits enable selfnet.de

mirrorbits add -country-only -http=https://mirrors.tuna.tsinghua.edu.cn/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ tsinghua.edu.cn
mirrorbits enable tsinghua.edu.cn

mirrorbits add -country-only -http=http://mirrors.ustc.edu.cn/msys2/ -rsync=rsync://rsync.mirrors.ustc.edu.cn/repo/msys2/ ustc.edu.cn
mirrorbits enable ustc.edu.cn

mirrorbits add -http=https://ftp.acc.umu.se/mirror/msys2.org/ -rsync=rsync://ftp.acc.umu.se/mirror/msys2.org/ umu.se
mirrorbits enable umu.se

mirrorbits add -http=https://quantum-mirror.hu/mirrors/pub/msys2/ -rsync=rsync://quantum-mirror.hu/msys2/ quantum-mirror.hu
mirrorbits enable quantum-mirror.hu

mirrorbits add -http=https://mirrors.dotsrc.org/msys2/ -rsync=rsync://mirrors.dotsrc.org/msys2/ dotsrc.org
mirrorbits enable dotsrc.org

mirrorbits add -http=https://mirror.ufro.cl/msys2/ -rsync=rsync://mirror.ufro.cl/msys2/ ufro.cl
mirrorbits enable ufro.cl

mirrorbits add -http=https://ftp.nluug.nl/pub/os/windows/msys2/builds/ -rsync=rsync://ftp.nluug.nl/msys2/builds/ nluug.nl
mirrorbits enable nluug.nl

mirrorbits add -http=https://download.nus.edu.sg/mirror/msys2/ -rsync=rsync://download.nus.edu.sg/msys2/ nus.edu.sg
mirrorbits enable nus.edu.sg

mirrorbits add -http=https://fastmirror.pp.ua/msys2/ -rsync=rsync://fastmirror.pp.ua/msys2/ fastmirror.pp.ua
mirrorbits enable fastmirror.pp.ua

mirrorbits add -http=https://mirror.clarkson.edu/msys2/ -rsync=rsync://mirror.clarkson.edu/msys2/ clarkson.edu
mirrorbits enable clarkson.edu

mirrorbits add -http=https://ftp.osuosl.org/pub/msys2/ -rsync=rsync://rsync.osuosl.org/msys2/ osuosl.org
mirrorbits enable osuosl.org
