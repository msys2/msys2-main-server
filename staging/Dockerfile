FROM elieux/ubuntu-pacman:5.2.2-ubuntu20.04 AS empty
RUN \
    apt update && \
    env DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        binutils \
        fakeroot \
    && \
    rm -Rf /var/{cache/apt,lib/apt/lists,log/{alternatives.log,apt,dpkg.log}} && \
true
RUN useradd -m -G users -s /usr/bin/bash builder
USER builder:users
WORKDIR /home/builder
COPY ./PKGBUILD.empty ./PKGBUILD
RUN makepkg


FROM elieux/ubuntu-pacman:5.2.2-ubuntu20.04
RUN \
    apt update && \
    env DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        git \
        gnupg \
        python3-pip \
        rsync \
    && \
    rm -Rf /var/{cache/apt,lib/apt/lists,log/{alternatives.log,apt,dpkg.log}} && \
true
VOLUME /srv/msys2staging
VOLUME /root/.gnupg
WORKDIR /root
COPY --from=empty /home/builder/__empty__-0-1-any.pkg.tar.gz ./
COPY ./runner.sh ./runner.sh
CMD [ "./runner.sh" ]
