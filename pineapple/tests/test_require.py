from unittest import TestCase

import pineapple

class TestRequire(TestCase):
    def test_none(self):
        s = pineapple.require()
        self.assertTrue(True)
    def test_builtins(self):
        pineapple.require('setuptools')
        self.assertTrue(True)
    def test_list(self):
        req = pineapple.require()
        flag = False
        for r in req:
            if r.startswith('setuptools=='):
                flag = True
        self.assertTrue(flag)
