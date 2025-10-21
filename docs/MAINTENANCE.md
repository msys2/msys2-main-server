# Maintenance

## Rebooting

```bash
ssh root@msys2.appfleet.io
# "up -d" all docker containers and see if everything works if re-created, to avoid changes there
reboot
# wait until it's up again (~1-2 minutes)
gpgconf --launch dirmngr
```

## Updating the Server

```bash
ssh root@msys2.appfleet.io
apt update
apt full-upgrade
```

```bash
# Update Python packages
pipx upgrade-all
uv tool upgrade --all
```

## Update Docker Services

```bash
ssh root@msys2.appfleet.io
cd /home/repo/msys2-main-server/
docker compose pull
docker compose build --parallel --no-cache
docker compose up -d
docker system prune --all --force
```

## Updating the Repo

```bash
cd msys2-devtools
./msys2-dbssh # connects via SSH

# Add packages to repo
export GPGKEY="5F944B027F7FE2091985AA2EFA11531AA0AA7F57"
msys2-autobuild fetch-assets --delete ./staging
./msys2-devtools/msys2-dbadd

# Prune repo (optional)
(cd msys2-devtools && uv run python msys2-repo-prune /srv/msys2repo/)

# Process package removals (if there are any)
(cd msys2-devtools && uv run python msys2-dbremove-api)

# Refresh mirrorbits after repo changes (will happen anyway every 5 minutes otherwise)
exit
ssh root@msys2.appfleet.io
(cd /home/repo/msys2-main-server/ && docker compose exec mirrorbits mirrorbits refresh)
```

## Removing old mirrorbits download stats

```bash
(cd /home/repo/msys2-main-server/ && docker compose exec mirrorbits mirrorbits-del-stats -f daily:1 monthly:1 yearly:1)
```

## Block an IP that is misusing the service

```bash
iptables -I DOCKER-USER 1 -s x.x.x.x -j REJECT
netfilter-persistent save
```

## Update installer

Pulls the installer from github and adjusts the "latest" symlinks.

```bash
./msys2-devtools/update-installer 2021-02-28
```
