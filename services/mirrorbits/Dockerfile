FROM ubuntu:jammy as build

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    pkg-config zlib1g-dev protobuf-compiler libprotoc-dev git make golang && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/etix/mirrorbits.git && \
    cd mirrorbits && \
    git checkout 7164f2c5e6f03e84f34612895ebd8218f741d1da

COPY 0001-Rework-the-mirror-selection-logic.patch mirrorbits

RUN cd mirrorbits && \
    git apply 0001-Rework-the-mirror-selection-logic.patch && \
    mkdir -p dist/usr/bin && \
    make install PREFIX=/usr DESTDIR=dist

RUN cd mirrorbits && \
    mkdir -p dist/usr/bin/contrib && \
    cp contrib/mirrorbits-geoupdate-all dist/usr/bin/ && \
    cp contrib/mirrorbits-del-stats dist/usr/bin/contrib/mirrorbits-del-stats

COPY mirrorbits-del-stats-wrapper.sh mirrorbits/dist/usr/bin/mirrorbits-del-stats

FROM ubuntu:jammy

COPY --from=build /mirrorbits/dist /

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    rsync redis-tools ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY init.sh /init.sh
CMD bash /init.sh
EXPOSE 80