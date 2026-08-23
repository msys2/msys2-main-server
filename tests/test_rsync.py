#!/usr/bin/env python3

import os
import unittest
import subprocess
import tempfile
from urllib.request import urlopen

from tests.utils import get_mirror_urls, get_rsync_command


class TestMirrors(unittest.TestCase):

    TIMEOUT = 75 if "CI" in os.environ else 25

    def test_mirrors_support_rsync(self):
        for rsync_url in sorted({rsync_url for _, rsync_url in get_mirror_urls()}):
            print(rsync_url)
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

if __name__ == '__main__':
    unittest.main()
