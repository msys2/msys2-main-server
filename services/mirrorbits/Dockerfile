FROM ubuntu:jammy as build

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    pkg-config zlib1g-dev protobuf-compiler libprotoc-dev git make golang && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/etix/mirrorbits.git && \
    cd mirrorbits && \
    git checkout 4e34d9b961a56bd669934acf1fd7d2313128a3d5

COPY 0001-Rework-the-mirror-selection-logic.patch mirrorbits
COPY 168.patch mirrorbits
COPY 169.patch mirrorbits

RUN cd mirrorbits && \
    git apply 0001-Rework-the-mirror-selection-logic.patch && \
    git apply 168.patch && \
    git apply 169.patch && \
    mkdir -p dist/usr/bin && \
    make install PREFIX=/usr DESTDIR=dist

FROM ubuntu:jammy

COPY --from=build /mirrorbits/dist /

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    rsync redis-tools ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY init.sh /init.sh
CMD bash /init.sh
EXPOSE 80