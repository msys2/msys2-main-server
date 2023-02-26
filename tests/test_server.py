#!/usr/bin/env python3

import os
import unittest
import subprocess
import itertools
from urllib.request import urlopen


class TestServer(unittest.TestCase):

    TIMEOUT = 75 if "CI" in os.environ else 25

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
