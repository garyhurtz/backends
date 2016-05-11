# -*- coding: utf-8 -*-
import unittest
from backends.FileSystemJsonBackend import FileSystemJsonBackend
from tests.JsonBackendTests import JsonBackendTestsEN, JsonBackendTestsZH
from tests import cachepath


class FileSystemJsonBackendENTestCase(unittest.TestCase, JsonBackendTestsEN):

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.clear()
        self.dut.dump(u'test', {u'a': 1})


class FileSystemJsonBackendZHTestCase(unittest.TestCase, JsonBackendTestsZH):

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.clear()
        self.dut.dump(u'中', {u'中': 1})


if __name__ == u'__main__':
    unittest.main()
