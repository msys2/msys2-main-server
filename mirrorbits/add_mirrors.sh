#!/bin/bash

mirrorbits add -http=https://repo.msys2.org/ -rsync=rsync://repo.msys2.org/builds/ msys2.org
mirrorbits enable msys2.org

mirrorbits add -http=https://mirror.yandex.ru/mirrors/msys2/ -rsync=rsync://mirror.yandex.ru/mirrors/msys2/ yandex.ru
mirrorbits enable yandex.ru

mirrorbits add -http=https://mirror.selfnet.de/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ selfnet.de
mirrorbits enable selfnet.de

mirrorbits add -country-only -http=https://mirrors.tuna.tsinghua.edu.cn/msys2/ -rsync=rsync://mirror.selfnet.de/msys2/ tsinghua.edu.cn
mirrorbits enable tsinghua.edu.cn

mirrorbits add -http=https://ftp.acc.umu.se/mirror/msys2.org/ -rsync=rsync://ftp.acc.umu.se/mirror/msys2.org/ umu.se
mirrorbits enable umu.se

mirrorbits add -http=https://quantum-mirror.hu/mirrors/pub/msys2/ -rsync=rsync://quantum-mirror.hu/msys2/ quantum-mirror.hu
mirrorbits enable quantum-mirror.hu

mirrorbits add -http=https://mirrors.dotsrc.org/msys2/ -rsync=rsync://mirrors.dotsrc.org/msys2/ dotsrc.org
mirrorbits enable dotsrc.org

mirrorbits add -http=https://mirror.ufro.cl/msys2/ -rsync=rsync://mirror.ufro.cl/msys2/ ufro.cl
mirrorbits enable ufro.cl