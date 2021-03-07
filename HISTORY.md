# How the server was set up

As *root*:

```bash
apt update
apt upgrade

apt install man

apt install git
cat >> ~/.profile
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi
export PS1='\[\e]0;\u@\h: \w\a\]\n${debian_chroot:+($debian_chroot)}\[\033[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]\n\[\e[1m\]#\[\e[0m\] '
^D

apt install mc
select-editor
echo "export EDITOR=mcedit" >> ~/.profile

dpkg-reconfigure locales
echo "export LANG=en_US.UTF-8" >> ~/.profile

dpkg-reconfigure tzdata

apt install unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

touch /etc/ssh/authorized_keys
chmod go+r /etc/ssh/authorized_keys
echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTLOxKnQyate/y7rJpUxKYUEzQTtQCIxEL7I7EMml0usJ1HsPwekQPMOhx4efX5j8NAtJPeBr9Yp9HR/rtV5vYDdRofyEaEIpsAY7ntxWHGSaFJBsM0Ln/BxjJYlrTDf/JFXjIDiCpYg82BIOHgoOdWh26TE/z7S2Pwjnz/3aFnDsc3QJ76Ibx122q9c0ysY6M5Bn7OznCn7//ks38hhSaq0hix4+aRcEU4OWuIf+0N52WZeOyxqg4JSIyNS5LdyuUHsYDZ/thMfoHYz3z310ayp3oRjrVsWUNMpjzbnzviLfxR4pBX9ZfqVMsVYeKlsygVrkp42qElrwPUdj8+eqsyVltxkOHl4GpPtUYhznnpy2sIsreOBVSN+wam05JeyU+kaOMDMbcguukcQXXieewYhQOVqB2J1daRWaWr+v4ziYuMZc9PaoqqqtToSOwT9gacN2ZBuU68pY/Jd49CmreDW0N3B2rsS9NujYTHiTOl6hI69uEOB4fzrl2+zo8RAk= lazka' >> /etc/ssh/authorized_keys
echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAgEAuwjmwYMkJrI31YmHVIx4D/6rkz3PjatRkd27PQDmP6DF54i0gTWZUaDVCGTf2JujNcdGKbPH4QpY2N69K8lG2T5dCrB61eTiYiF7H+xXV3fuVIhq7JLjg4IEkSp3i5QPjECbq0HYbmMaehZwo+ChuaO/D6rp/okoZTkJU21OCbch9y0n3t0qOLdfoFfVrXpwl5DVFZraXqo2BwRhI5plj3M6BxQl30tiqrz5U1lcJe6ZpigbqbajQqK2Z946UpqxjxN/kT3Vw6epj00F8phJdxyAKHCuQohVTm31j1z21c1qjlGpnV2UtnMVL+2/MtksvGtrSW6HPrv1IIze5UiELL12ObJezf+rAnrLcldXE9YglQC+coEvPzwhUIntdz8IP5wzk29nzeVaoNaHym2GyTi+FWzma1dHpoPW9vGAhOa7t2zXs6kPLyZwMWidLOpeG8ZEoVpDZbzCZdZzcfVFbwwzzE8Zo/+oZCriqTPlncc/HkQuTyjKxYfTMY+bdxx2o/zaHVNscX6GBsKw7j74+3h+Q7/baKvdo3QAawolyl1JMzvMkMskAvsbuF7UWQ5MPOTUKUZKlHvUoxjWPzTnepOSvWc6kJEMr/ZtEY6H3/VqqRkcdho4CmG8I7c7hstwls2JvQxVX3lYB1s5fH3GMAHHUvh4CH3M1pDruxFub9k= elieux' >> /etc/ssh/authorized_keys
sed -i /etc/ssh/sshd_config -e $'/^AuthorizedKeysFile/{ s/^/#/; a AuthorizedKeysFile /etc/ssh/authorized_keys .ssh/authorized_keys\n }'
service ssh reload

iptables -F
ip6tables -F
iptables -A INPUT -i lo -j ACCEPT
ip6tables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -s 127.0.0.0/8 -j DROP
ip6tables -A INPUT -s ::1/128 -j DROP
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -m state --state INVALID -j REJECT
ip6tables -A INPUT -m state --state INVALID -j REJECT
iptables -A INPUT -p tcp --dport ssh -j ACCEPT
ip6tables -A INPUT -p tcp --dport ssh -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
ip6tables -A INPUT -p icmpv6 -j ACCEPT
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
ip6tables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "ip6tables denied: " --log-level 7
iptables -A INPUT -j REJECT
ip6tables -A INPUT -j REJECT
iptables -P FORWARD DROP
ip6tables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
ip6tables -P OUTPUT ACCEPT

apt install iptables-persistent
dpkg-reconfigure -plow iptables-persistent

apt install vnstat
sed -i /etc/vnstat.conf -e 's/^Interface ""$/Interface "enp2s0"/'
systemctl restart vnstat
vnstat --iflist | sed -e 's/^Available interfaces: //' -e 's/(.*)//g' -e 's/enp2s0//' | xargs -rn1 vnstat --remove --force --iface

useradd -s /bin/bash repo
usermod -p '*' repo
mkdir /home/repo
chown -R repo:repo /home/repo
chmod go-rwx -R /home/repo
```

As `repo`:

```bash
cat >> ~/.profile
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi
. /usr/lib/git-core/git-sh-prompt
export PS1='\[\e]0;\u@\h: \w\a\]\n${debian_chroot:+($debian_chroot)}\[\033[32m\]\u@\h \[\e[33m\]\w\[\e[0m\]$(__git_ps1 " (%s)")\n\[\e[1m\]$\[\e[0m\] '
^D
select-editor
echo "export EDITOR=mcedit" >> ~/.profile
echo "export LANG=en_US.UTF-8" >> ~/.profile

sudo apt install rsync
sudo mkdir /srv/msys2repo
sudo chown repo:repo /srv/msys2repo
rsync -rtlvH --delete-after --delay-updates --safe-links rsync://repo.msys2.org/builds/ /srv/msys2repo/

sudo apt install docker.io docker-compose
sudo iptables -I INPUT 5 -p tcp -m multiport --dports http,https,rsync -j ACCEPT
sudo ip6tables -I INPUT 5 -p tcp -m multiport --dports http,https,rsync -j ACCEPT
sudo dpkg-reconfigure -plow iptables-persistent
git clone https://github.com/msys2/msys2-main-server
echo "GITHUB_TOKEN=<token from https://github.com/settings/tokens with nothing enabled>" > msys2-main-server/github_token.env
sudo docker-compose up -d --build -f msys2-main-server/docker-compose.yml --project-directory msys2-main-server

sudo apt install gnupg
gpg --update-trustdb
curl -L https://github.com/msys2/msys2-keyring/raw/master/msys2.gpg | gpg --import
echo $'5\ny\n' | gpg --command-fd 0 --no-tty --edit-key 87771331B3F1FF5263856A6D974C8BE49078F532 trust
echo $'5\ny\n' | gpg --command-fd 0 --no-tty --edit-key 5F944B027F7FE2091985AA2EFA11531AA0AA7F57 trust
cat > .gnupg/gpg.conf
no-greeting
require-cross-certification
charset utf-8
utf8-strings
no-mangle-dos-filenames
keyserver-options auto-key-retrieve
#keyserver-options no-self-sigs-only
keyserver-options no-import-clean
# From https://github.com/ioerror/duraconf/blob/master/configs/gnupg/gpg.conf
no-emit-version
no-comments
keyid-format 0xlong
with-fingerprint
list-options show-uid-validity
verify-options show-uid-validity
use-agent
no-autostart
keyserver-options no-honor-keyserver-url
keyserver-options include-revoked
# Intersection
# From https://sparkslinux.wordpress.com/2013/02/21/hashing-algorithm-is-your-gpg-configuration-secure/
# From https://github.com/ioerror/duraconf/blob/master/configs/gnupg/gpg.conf
personal-cipher-preferences AES256 AES192 AES
personal-digest-preferences SHA512 SHA384 SHA256
personal-compress-preferences ZLIB BZIP2 ZIP Uncompressed
cert-digest-algo SHA512
# Composed from above personal preferences
default-preference-list SHA512 SHA384 SHA256 AES256 AES192 AES ZLIB BZIP2 ZIP Uncompressed
^D
echo StreamLocalBindUnlink yes | sudo tee -a /etc/ssh/sshd_config
sudo service ssh reload

sudo apt install python3-pip
echo "export $(cat msys2-main-server/github_token.env)" >> ~/.profile
git clone https://github.com/msys2/msys2-autobuild
pip3 install -r msys2-autobuild/requirements.txt
git clone https://github.com/msys2/msys2-devtools
mkdir -p staging/{mingw,msys}/{sources,i686,x86_64}/
docker run --name ubuntu-pacman --rm -it elieux/ubuntu-pacman:5.2.2-ubuntu20.04 # in a separate session
sudo apt install libarchive13 libarchive-tools libcurl4 libgpgme11 libssl1.1
sudo docker exec ubuntu-pacman tar -czf - /etc/{makepkg,pacman}.conf /var/cache/pacman/pkg /var/lib/pacman/ /usr/local/{bin,include,lib,share} | sudo tar -xzf - -C /
sudo ldconfig
sudo pacman
```
