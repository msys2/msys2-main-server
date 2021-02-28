FROM ubuntu:20.04

RUN \
    apt update && \
    env DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
        apache2 \
        composer \
        curl \
        libapache2-mod-php7.4 \
        patchutils \
        unzip \
    && \
    rm -Rf /var/{cache/apt,lib/apt/lists,log/{alternatives.log,apt,dpkg.log}} && \
true

WORKDIR /var/www/html/
RUN rm index.html
RUN curl -sL https://github.com/alexandermarston/vnstat-dashboard/archive/master.tar.gz | tar -xzf - --wildcards --strip-components=2 'vnstat-dashboard-master/app/*'
COPY *.patch ./
RUN echo *.patch | xargs -rn1 patch -p2 -i && rm *.patch
RUN composer install
RUN mkdir -m=0777 templates_c/

VOLUME /var/lib/vnstat/
EXPOSE 80
RUN sed -e '/^*)/ { n; s/$HTTPD/exec &/; }' -i /usr/sbin/apache2ctl
ENTRYPOINT [ "apache2ctl" ]
CMD [ "-DFOREGROUND" ]
