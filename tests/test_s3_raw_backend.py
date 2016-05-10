# -*- coding: UTF-8 -*- #
import unittest
from backends.S3RawBackend import S3RawBackend
from tests.RawBackendTests import RawBackendTests


class TestS3RawBackend(unittest.TestCase, RawBackendTests):

    def setUp(self):
        self.dut = S3RawBackend(u'test-stellour')

        with open(u'main.css', u'r') as infile:
            self.dut.dump(u'test', infile)

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)
