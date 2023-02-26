#!/usr/bin/env python3

import os
import re
import unittest
import subprocess
import itertools
import ssl
from urllib.request import urlopen


def get_mirrors():
    """Returns a list of URLs for all our mirrors"""

    DIR = os.path.dirname(os.path.realpath(__file__))
    mirrors = set()
    script = os.path.join(DIR, "..", "services", "mirrorbits", "add_mirrors.sh")
    with open(script, "r", encoding="utf-8") as h:
        for line in h.readlines():
            if line.startswith("#"):
                continue
            mirrors.update(
                re.findall('((?:http|https)://[a-zA-Z0-9./?=_%:-]*)', line))
    return sorted(mirrors)


def get_timeout():
    timeout = 25
    if "CI" in os.environ:
        timeout *= 4
    return timeout


class Test(unittest.TestCase):

    TIMEOUT = get_timeout()

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

    def assertHSTS(self, response):
        self.assertTrue(response.headers.get("Strict-Transport-Security"))

    def test_rsync(self):
        out = subprocess.check_output(
            ["rsync", "--list-only", "rsync://repo.msys2.org/builds/"],
            universal_newlines=True,
            timeout=self.TIMEOUT)
        self.assertTrue("distrib" in out)
        self.assertTrue("mingw" in out)
        self.assertTrue("msys" in out)

    def test_repo(self):
        with urlopen("https://repo.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org")
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("distrib" in out)
            self.assertTrue("mingw" in out)
            self.assertTrue("msys" in out)

    def test_repo_redirects(self):
        with urlopen("https://repo.msys2.org/mingw/sources", timeout=self.TIMEOUT) as r:
            self.assertHSTS(r)
            self.assertEqual(r.url, "https://repo.msys2.org/mingw/sources/")
        with urlopen("http://repo.msys2.org/mingw/sources", timeout=self.TIMEOUT) as r:
            self.assertHSTS(r)
            self.assertEqual(r.url, "https://repo.msys2.org/mingw/sources/")

    def test_stagingrepo(self):
        with urlopen("https://repo.msys2.org/staging/", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/staging/")
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("staging.db" in out)
        with urlopen("https://repo.msys2.org/staging", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/staging/")
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("staging.db" in out)
        with urlopen("http://repo.msys2.org/staging", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/staging/")
            self.assertHSTS(r)
        with urlopen("http://repo.msys2.org/staging/", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/staging/")
            self.assertHSTS(r)

    def test_stats(self):
        with urlopen("https://repo.msys2.org/stats/", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/stats/")
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("Network Traffic" in out)
        with urlopen("https://repo.msys2.org/stats", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/stats/")
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("Network Traffic" in out)
        with urlopen("http://repo.msys2.org/stats/", timeout=self.TIMEOUT) as r:
            self.assertEqual(r.url, "https://repo.msys2.org/stats/")
            self.assertHSTS(r)

    def test_redirects(self):
        schemes = ["http", "https"]
        variants = ["www.", ""]
        tlds = ["org", "com", "net"]
        for scheme, tld, variant in itertools.product(schemes, tlds, variants):
            url = f"{scheme}://{variant}msys2.{tld}"
            with urlopen(url, timeout=self.TIMEOUT) as r:
                self.assertTrue(r.url.startswith("https://www.msys2.org"))
                self.assertEqual(r.status, 200)
        tlds = ["org", "net"]
        for scheme, tld, variant in itertools.product(schemes, tlds, variants):
            url = f"{scheme}://{variant}mingw-w64.{tld}"
            with urlopen(url, timeout=self.TIMEOUT) as r:
                self.assertTrue(r.url.startswith("https://www.mingw-w64.org"))
                self.assertEqual(r.status, 200)

    def test_packages(self):
        with urlopen("http://packages.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org"))
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("<html" in out)
        with urlopen("https://packages.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org"))
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("<html" in out)
        with urlopen("https://packages.msys2.org/api", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org/api"))
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("<html" in out)
        with urlopen("http://packages.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertHSTS(r)
            self.assertTrue(r.url.startswith("https://packages.msys2.org"))

    def test_mirror(self):
        with urlopen("http://mirror.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://repo.msys2.org"))
            self.assertHSTS(r)
            out = r.read().decode()
            self.assertTrue("distrib" in out)
            self.assertTrue("mingw" in out)
            self.assertTrue("msys" in out)

if __name__ == '__main__':
    unittest.main()