# -*- coding: UTF-8 -*- #
import unittest

from tests.BackendTests import BackendTests

__author__ = 'gary'


class RawBackendTests(BackendTests):

    @unittest.expectedFailure
    def test_is_gzipped(self):
        """
        Need a clean way to confirm that the file was gzipped
        :return:
        """

        raise NotImplementedError()

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
        self.assertIsInstance(self.dut.load(u'test'), basestring)

    def test_dump_fp(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)

        with open(u'main.css', u'r') as infile:
            self.assertTrue(self.dut.dump(u'test2', infile))

        self.assertEqual(1, len(self.dut) - before)

    def test_dump_ascii_string(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)

        self.assertTrue(self.dut.dump(u'test2', u'this is a test string'))

        self.assertEqual(1, len(self.dut) - before)

    def test_dump_unicode_string(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)

        self.assertTrue(self.dut.dump(u'test2', u'中文'))

        self.assertEqual(1, len(self.dut) - before)

    def test_delete(self):
        """
        Delete a value from the backend
        """
        before = len(self.dut)
        self.assertTrue(self.dut.delete(u'test'))
        self.assertEqual(1, before - len(self.dut))
