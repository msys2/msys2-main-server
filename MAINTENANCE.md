# Maintenance

# Rebooting

```bash
# "up -d" all docker containers and see if everything works if re-created, to avoid changes there
reboot
# wait until it's up again
gpgconf --launch dirmngr
```

# Updating the Repo

```bash
cd msys2-devtools
./msys2-dbssh # connects via SSH

# Add packages to repo
export GPGKEY="5F944B027F7FE2091985AA2EFA11531AA0AA7F57"
./msys2-autobuild/autobuild.py fetch-assets --delete ./staging
./msys2-devtools/msys2-dbadd

# Prune repo (optional)
./msys2-devtools/msys2-repo-prune /srv/msys2repo/

# Process package removals (if there are any)
./msys2-devtools/msys2-dbremove-api

# Refresh mirrorbits after repo changes
exit
ssh root@msys2.appfleet.io
cd /home/repo/msys2-main-server/
docker-compose exec mirrorbits mirrorbits refresh
```