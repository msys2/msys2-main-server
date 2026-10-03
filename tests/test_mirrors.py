#!/usr/bin/env python3

import os
import re
import unittest
import ssl
import subprocess
import tempfile
import time
from urllib.request import urlopen


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


class TestMirrors(unittest.TestCase):

    TIMEOUT = 75 if "CI" in os.environ else 25

    def test_mirrors_support_tls12(self):
        # https://github.com/msys2/msys2.github.io/issues/204
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        for url in get_mirrors():
            somefile = url.rstrip("/") + "/lastsync"
            try:
                with urlopen(somefile, context=context, timeout=self.TIMEOUT):
                    pass
            except Exception as exc:
                raise Exception(somefile) from exc

    def test_mirrors_support_rsync(self):
        for rsync_url in sorted({rsync_url for _, rsync_url in get_mirror_urls()}):
            print(rsync_url)
            # This endpoint only accepts connections from the main server.
            if rsync_url == "rsync://us.dyi.ng/msys2/" and not os.path.isdir("/srv/msys2repo"):
                continue

            rsync_command, actual_url = get_rsync_command(rsync_url)
            try:
                subprocess.check_call(
                    [rsync_command, "--list-only", actual_url.rstrip("/") + "/lastsync"],
                    stdout=subprocess.DEVNULL,
                    timeout=self.TIMEOUT)
            except Exception as exc:
                raise Exception(rsync_url) from exc

    def test_rsync_not_newer_than_http(self):
        # https://github.com/msys2/msys2-main-server/issues/76
        for http_url, rsync_url in get_mirror_urls():
            print(http_url, rsync_url)
            # This endpoint only accepts connections from the main server.
            if rsync_url == "rsync://us.dyi.ng/msys2/" and not os.path.isdir("/srv/msys2repo"):
                continue

            rsync_command, actual_url = get_rsync_command(rsync_url)

            with tempfile.TemporaryDirectory() as tempdir:
                try:
                    subprocess.check_call(
                        [rsync_command, actual_url.rstrip("/") + "/lastsync", "lastsync"],
                        cwd=tempdir,
                        stdout=subprocess.DEVNULL,
                        timeout=self.TIMEOUT)
                    with open(os.path.join(tempdir, "lastsync"), encoding="utf-8") as f:
                        rsync_lastsync = int(f.read())

                    with urlopen(http_url.rstrip("/") + "/lastsync", timeout=self.TIMEOUT) as f:
                        http_lastsync = int(f.read())
                except Exception as exc:
                    raise Exception(f"{http_url} ({rsync_url})") from exc

            self.assertLessEqual(rsync_lastsync, http_lastsync, http_url)

    def test_download_speed(self):
        # https://github.com/msys2/msys2.github.io/issues/276
        for url in get_mirrors():
            somelargefile = url.rstrip("/") + "/distrib/msys2-x86_64-latest.tar.xz"

            chunk_size = 1024 * 50
            chunks = 50
            read_timeout = chunk_size * chunks / 100000
            try:
                with urlopen(somelargefile, timeout=self.TIMEOUT) as f:
                    rt = time.time()
                    for i in range(chunks):
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        if time.time() - rt > read_timeout:
                            raise Exception("Read timeout")
            except Exception as exc:
                raise Exception(somelargefile) from exc
            else:
                duration = time.time() - rt
                print("Downloading:", chunk_size * chunks / (1024 ** 2), "MB, in", duration, ",timeout:", read_timeout, somelargefile)

if __name__ == '__main__':
    unittest.main()
