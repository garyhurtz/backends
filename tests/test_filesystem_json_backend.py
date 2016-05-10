# -*- coding: utf-8 -*-
import unittest

from backends.FileSystemJsonBackend import FileSystemJsonBackend
from JsonBackendTests import JsonBackendTestsZH
from tests.JsonBackendTests import JsonBackendTestsEN, JsonBackendTestsZH
from tests import cachepath


class FileSystemJsonBackendENTestCase(unittest.TestCase, JsonBackendTestsEN):

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.dump(u'test', {u'a': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


class FileSystemJsonBackendZHTestCase(unittest.TestCase, JsonBackendTestsZH):

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.dump(u'中', {u'中': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


if __name__ == u'__main__':
    unittest.main()
