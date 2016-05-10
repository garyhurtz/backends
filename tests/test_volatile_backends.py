# -*- coding: UTF-8 -*- #
import unittest
from backends.VolatileBackend import VolatileBackend
from tests.JsonBackendTests import JsonBackendTestsEN, JsonBackendTestsZH


class TestVolatileBackend(unittest.TestCase, JsonBackendTestsEN):

    def setUp(self):
        self.dut = VolatileBackend()
        self.dut.dump(u'test', {u'a': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)


class TestVolatileBackendZH(unittest.TestCase, JsonBackendTestsZH):

    def setUp(self):
        self.dut = VolatileBackend()
        self.dut.dump(u'中', {u'中': 1})

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating
        for key in [key for key in self.dut]:
            self.dut.delete(key)
