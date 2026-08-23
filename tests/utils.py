
import os
import re


def get_mirror_urls():
    """Returns the HTTP and rsync URLs for all our mirrors"""

    DIR = os.path.dirname(os.path.realpath(__file__))
    mirrors = set()
    script = os.path.join(DIR, "..", "services", "mirrorbits", "add_mirrors.sh")
    with open(script, "r", encoding="utf-8") as h:
        for line in h.readlines():
            if line.startswith("#"):
                continue
            mirrors.update(re.findall(
                r'-http=(https?://\S+) -rsync=(rsyncs?://\S+)', line))
    return sorted(mirrors)


def get_mirrors():
    """Returns a list of HTTP URLs for all our mirrors"""

    return [http_url for http_url, _ in get_mirror_urls()]


def get_rsync_command(rsync_url):
    if rsync_url.startswith("rsyncs://"):
        return "rsync-ssl", "rsync://" + rsync_url.removeprefix("rsyncs://")
    return "rsync", rsync_url
