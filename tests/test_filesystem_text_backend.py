# -*- coding: utf-8 -*-
import unittest
import codecs

from backends.FileSystemTextBackend import FileSystemTextBackend
from tests import cachepath


class FileSystemTextFileBackendTestCase(unittest.TestCase):

    def setUp(self):
        self.dut = FileSystemTextBackend(cachepath)

        with codecs.open(u'main.css', u'r', u'utf-8') as value:
            self.dut.dump(u'test', value)
            self.dut.dump(u'考', value)

    def tearDown(self):
        # make a copy of the key set to avoid changes while iterating

        for key in [key for key in self.dut]:
            self.dut.delete(key)

    def test_contains(self):
        """
        Return True if key is in the backend, else False
        :param key:
        :return:
        """
        self.assertTrue(u'test' in self.dut)
        self.assertTrue(u'考' in self.dut)

    def test_keys(self):
        """
        Dict-like retrieval of all keys in the backend
        """
        self.assertTrue(u'test' in self.dut.keys())
        self.assertTrue(u'考' in self.dut.keys())

    def test_load(self):
        """
        Retrieve a value from the backend
        """
        self.assertIsInstance(self.dut.load(u'test'), basestring)
        self.assertIsInstance(self.dut.load(u'考'), basestring)

    def test_dump(self):
        """
        Store a value in the backend
        """
        before = len(self.dut)

        with codecs.open(u'main.css', u'r', u'utf-8') as infile:
            value = infile.read()

        self.dut.dump(u'test2', value)
        self.dut.dump(u'考2', value)
        self.assertEqual(2, len(self.dut) - before)

    def test_delete(self):
        """
        Delete a value from the backend
        """
        before = len(self.dut)

        self.assertTrue(self.dut.delete(u'test'))
        self.assertTrue(self.dut.delete(u'考'))

        self.assertEqual(2, before - len(self.dut))
