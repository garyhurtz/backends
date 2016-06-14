# -*- coding: UTF-8 -*- #
import unittest
from backends.VolatileBackend import VolatileBackend
from tests.JsonBackendTests import JsonBackendTests


class TestVolatileBackend(unittest.TestCase, JsonBackendTests):

    key = u'test'

    def setUp(self):
        self.dut = VolatileBackend()
        self.dut.dump(self.key, {u'a': 1})

    def tearDown(self):
        self.dut.clear()


class TestVolatileBackendZH(unittest.TestCase, JsonBackendTests):

    key = u'中'

    def setUp(self):
        self.dut = VolatileBackend()
        self.dut.dump(self.key, {u'芭': 1})

    def tearDown(self):
        self.dut.clear()
