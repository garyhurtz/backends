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
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


class TestVolatileBackendZH(unittest.TestCase, JsonBackendTests):

    key = u'中'

    def setUp(self):
        self.dut = VolatileBackend()
        self.dut.dump(self.key, {u'芭': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)
