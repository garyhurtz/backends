# -*- coding: UTF-8 -*- #
import unittest

from backends.S3JsonBackend import S3JsonBackend
from tests.JsonBackendTests import JsonBackendTestsEN, JsonBackendTestsZH


class S3JsonBackendENTestCase(unittest.TestCase, JsonBackendTestsEN):

    def setUp(self):

        self.dut = S3JsonBackend(u'test-stellour')

        self.dut.dump(u'test', {u'a': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


class S3JsonBackendZHTestCase(unittest.TestCase, JsonBackendTestsZH):

    def setUp(self):
        self.dut = S3JsonBackend(u'test-stellour')

        self.dut.dump(u'中', {u'中': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)

