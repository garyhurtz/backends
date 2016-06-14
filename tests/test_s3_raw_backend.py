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
        self.dut.clear()
