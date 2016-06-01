# -*- coding: UTF-8 -*- #
import unittest

from backends.S3JsonBackend import S3JsonBackend
from tests.JsonBackendTests import JsonBackendTests


class S3JsonBackendENTestCase(unittest.TestCase, JsonBackendTests):

    key = u'test'

    def setUp(self):

        self.dut = S3JsonBackend(u'test-stellour')

        self.dut.dump(self.key, {u'a': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


class S3JsonBackendZHTestCase(unittest.TestCase, JsonBackendTests):

    key = u'中'

    def setUp(self):
        self.dut = S3JsonBackend(u'test-stellour')

        self.dut.dump(self.key, {u'芭': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)

