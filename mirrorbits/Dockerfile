FROM ubuntu:focal as build

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    pkg-config zlib1g-dev protobuf-compiler libprotoc-dev git make golang && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/etix/mirrorbits.git && \
    cd mirrorbits && \
    git checkout eeea0e026d0ca99c7009a91a54369f7c29e87049

COPY 0001-Rework-the-mirror-selection-logic.patch mirrorbits

RUN cd mirrorbits && \
    git apply 0001-Rework-the-mirror-selection-logic.patch && \
    mkdir -p dist/usr/bin && \
    make install PREFIX=/usr DESTDIR=dist

FROM ubuntu:focal

COPY --from=build /mirrorbits/dist /

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    rsync redis-tools ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY init.sh /init.sh
CMD bash /init.sh
EXPOSE 80