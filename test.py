#!/usr/bin/env python3

import unittest
import subprocess
import itertools
from urllib.request import urlopen


class Test(unittest.TestCase):

    TIMEOUT = 10

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
            out = r.read().decode()
            self.assertTrue("distrib" in out)
            self.assertTrue("mingw" in out)
            self.assertTrue("msys" in out)

    def test_redirects(self):
        schemes = ["http", "https"]
        tlds = ["org", "com", "net"]
        variants = ["www.", ""]
        for scheme, tld, variant in itertools.product(schemes, tlds, variants):
            url = f"{scheme}://{variant}msys2.{tld}"
            with urlopen(url, timeout=self.TIMEOUT) as r:
                self.assertTrue(r.url.startswith("https://www.msys2.org"))
                self.assertEqual(r.status, 200)

    def test_packages(self):
        with urlopen("http://packages.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org"))
            out = r.read().decode()
            self.assertTrue("<html" in out)
        with urlopen("https://packages.msys2.org", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org"))
            self.assertTrue("<html" in out)
        with urlopen("https://packages.msys2.org/api", timeout=self.TIMEOUT) as r:
            self.assertTrue(r.url.startswith("https://packages.msys2.org/api"))
            self.assertTrue("<html" in out)


if __name__ == '__main__':
    unittest.main()