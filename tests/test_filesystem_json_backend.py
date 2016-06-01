# -*- coding: utf-8 -*-
import unittest
from backends.FileSystemJsonBackend import FileSystemJsonBackend
from tests.JsonBackendTests import JsonBackendTests
from tests import cachepath


class FileSystemJsonBackendENTestCase(unittest.TestCase, JsonBackendTests):

    key = u'test'

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.clear()
        self.dut.dump(self.key, {u'a': 1})


class FileSystemJsonBackendZHTestCase(unittest.TestCase, JsonBackendTests):

    key = u'中'

    def setUp(self):
        self.dut = FileSystemJsonBackend(cachepath)
        self.dut.clear()
        self.dut.dump(self.key, {u'芭': 1})


if __name__ == u'__main__':
    unittest.main()
