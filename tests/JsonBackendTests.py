# -*- coding: UTF-8 -*- #
from tests.BackendTests import BackendTests

__author__ = 'gary'


class JsonBackendTestsEN(BackendTests):

    def test_contains(self):
        """
        Return True if key is in the backend, else False
        :param key:
        :return:
        """
        self.assertTrue(u'test' in self.dut)

    def test_keys(self):
        """
        Dict-like retrieval of all keys in the backend
        """
        self.assertTrue(u'test' in self.dut.keys())

    def test_load(self):
        """
        Retrieve a value from the backend
        """
        self.assertIsInstance(self.dut.load(u'test'), dict)

    def test_dump(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.dump(u'test2', {u'b': 2}))
        self.assertEqual(1, len(self.dut) - before)

    def test_delete(self):
        """
        Delete a value from the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.delete(u'test'))
        self.assertEqual(1, before - len(self.dut))


class JsonBackendTestsZH(BackendTests):

    def test_contains(self):
        """
        Return True if key is in the backend, else False
        :param key:
        :return:
        """
        self.assertTrue(u'中' in self.dut)

    def test_keys(self):
        """
        Dict-like retrieval of all keys in the backend
        """
        self.assertTrue(u'中' in self.dut.keys())

    def test_load(self):
        """
        Retrieve a value from the backend
        """
        self.assertIsInstance(self.dut.load(u'中'), dict)

    def test_dump(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.dump(u'中2', {u'b': 2}))
        self.assertEqual(1, len(self.dut) - before)

    def test_delete(self):
        """
        Delete a value from the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.delete(u'中'))
        self.assertEqual(1, before - len(self.dut))
