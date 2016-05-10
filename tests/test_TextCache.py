# -*- coding: utf-8 -*-
import unittest
import codecs
from backends.TextCache import TextCache

from tests import cachepath


class TestTextCache(unittest.TestCase):

    def setUp(self):
        self.dut = TextCache(cachepath)

        with codecs.open(u'en.txt', u'r', u'utf-8') as infile:
            self.en = infile
            self.dut.set(u'en', infile)

        with codecs.open(u'中文.txt', u'r', u'utf-8') as infile:
            self.zh = infile
            self.dut.set(u'中文', infile)

    def tearDown(self):
        """
        Clean up cached items
        :return:
        """
        for key in [key for key in self.dut.keys()]:
            self.dut.delete(key)

    def test_get_en(self):

        self.assertTrue(u'en' in self.dut.locals)
        self.assertTrue(u'en' in self.dut)

        self.assertEquals(self.dut.get(u'en'), self.en)

    def test_get_zh(self):

        self.assertTrue(u'中文' in self.dut.locals)
        self.assertTrue(u'中文' in self.dut)

        self.assertEquals(self.dut.get(u'中文'), self.zh)

    def test_set(self):
        len_before = len(self.dut.keys())
        self.dut.set(u'test', self.en)
        self.assertEqual(1, len(self.dut.keys()) - len_before)

    def test_keys(self):

        keys = self.dut.keys()

        self.assertTrue(isinstance(keys, set))
        self.assertEqual(2, len(keys))

    def test_items(self):
        self.assertEqual(2, len(list(self.dut.items())))

    def test_contains_en(self):
        self.assertTrue(u'en' in self.dut)

    def test_contains_zh(self):
        self.assertTrue(u'中文' in self.dut)

    def test_len(self):
        self.assertEqual(2, len(self.dut))

    def test_clear(self):
        self.assertEqual(2, len(self.dut))
        self.dut.clear()
        self.assertEqual(0, len(self.dut))

if __name__ == u'__main__':
    unittest.main()
