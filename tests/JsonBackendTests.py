# -*- coding: UTF-8 -*- #
from tests.BackendTests import BackendTests
import unittest
__author__ = u'gary'


class JsonBackendTests(BackendTests):

    key = None

    def test_contains(self):
        """
        Return True if key is in the backend, else False
        :param key:
        :return:
        """
        self.assertTrue(self.key in self.dut)

    @unittest.expectedFailure
    def test_keys(self):
        """
        Dict-like retrieval of all keys in the backend
        """
        self.assertTrue(self.key in self.dut.keys())

    def test_load(self):
        """
        Retrieve a value from the backend
        """
        self.assertIsInstance(self.dut.load(self.key), dict)

    def test_dump(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.dump(self.key + u'2', {u'b': 2}))
        self.assertEqual(1, len(self.dut) - before)

    def test_delete(self):
        """
        Delete a value from the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.delete(self.key))
        self.assertEqual(1, before - len(self.dut))
