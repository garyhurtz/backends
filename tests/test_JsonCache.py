# -*- coding: utf-8 -*-
import unittest
from backends.JsonCache import JsonCache

from tests import cachepath


class TestJsonCache(unittest.TestCase):

    def setUp(self):
        self.dut = JsonCache(cachepath)
        self.dut.clear()

    def test_get_en(self):
        value = {u'key': u'value'}

        self.dut.set(u'test', value)

        self.assertTrue(u'test' in self.dut.locals)
        self.assertTrue(u'test' in self.dut)

        self.assertEquals(self.dut.get(u'test'), value)

    def test_get_zh(self):
        value = {u'这': u'个'}

        self.dut.set(u'考', value)

        self.assertTrue(u'考' in self.dut.locals)
        self.assertTrue(u'考' in self.dut)

        self.assertEquals(self.dut.get(u'考'), value)

    def test_set(self):
        len_before = len(self.dut.keys())
        self.dut.set(u'test2', {u'key': u'value'})
        self.assertEqual(1, len(self.dut.keys()) - len_before)

    def test_keys(self):
        self.dut.set(u'test', {u'key': u'value'})
        self.dut.set(u'考', {u'这': u'个'})

        keys = self.dut.keys()

        self.assertTrue(isinstance(keys, set))
        self.assertEqual(2, len(keys))

    def test_items(self):
        self.dut.set(u'test', {u'key': u'value'})
        self.dut.set(u'考', {u'这': u'个'})
        self.assertEqual(2, len(list(self.dut.items())))

    def test_contains_en(self):
        self.dut.set(u'test', {u'key': u'value'})
        self.assertTrue(u'test' in self.dut)

    def test_contains_zh(self):
        self.dut.set(u'考', {u'这': u'个'})
        self.assertTrue(u'考' in self.dut)

    def test_len(self):
        self.dut.set(u'test', {u'key': u'value'})
        self.dut.set(u'考', {u'这': u'个'})
        self.assertEqual(2, len(self.dut))

    def test_clear(self):
        self.dut.set(u'test', {u'key': u'value'})
        self.dut.set(u'考', {u'这': u'个'})
        self.assertEqual(2, len(self.dut))
        self.dut.clear()
        self.assertEqual(0, len(self.dut))


class TestJsonCacheNested(unittest.TestCase):

    def setUp(self):
        self.dut = JsonCache(cachepath)
        self.dut.clear()

    def test_get_en(self):
        value = {u'key': u'value'}

        self.dut.set(u'subdir/test', value)

        self.assertTrue(u'subdir/test' in self.dut.locals)
        self.assertTrue(u'subdir/test' in self.dut)

        self.assertEquals(self.dut.get(u'subdir/test'), value)

    def test_get_zh(self):
        value = {u'这': u'个'}

        self.dut.set(u'什么/考', value)

        self.assertTrue(u'什么/考' in self.dut.locals)
        self.assertTrue(u'什么/考' in self.dut)

        self.assertEquals(self.dut.get(u'什么/考'), value)

    def test_set(self):
        len_before = len(self.dut.keys())
        self.dut.set(u'subdir/test2', {u'key': u'value'})
        self.assertEqual(1, len(self.dut.keys()) - len_before)

    def test_keys(self):
        self.dut.set(u'subdir/test', {u'key': u'value'})
        self.dut.set(u'什么/考', {u'这': u'个'})

        keys = self.dut.keys()

        self.assertTrue(isinstance(keys, set))
        self.assertEqual(2, len(keys))

    def test_items(self):
        self.dut.set(u'subdir/test', {u'key': u'value'})
        self.dut.set(u'什么/考', {u'这': u'个'})
        self.assertEqual(2, len(list(self.dut.items())))

    def test_contains_en(self):
        self.dut.set(u'subdir/test', {u'key': u'value'})
        self.assertTrue(u'subdir/test' in self.dut)

    def test_contains_zh(self):
        self.dut.set(u'什么/考', {u'这': u'个'})
        self.assertTrue(u'什么/考' in self.dut)

    def test_len(self):
        self.dut.set(u'subdir/test', {u'key': u'value'})
        self.dut.set(u'什么/考', {u'这': u'个'})
        self.assertEqual(2, len(self.dut))

    def test_clear(self):
        self.dut.set(u'subdir/test', {u'key': u'value'})
        self.dut.set(u'什么/考', {u'这': u'个'})
        self.assertEqual(2, len(self.dut))
        self.dut.clear()
        self.assertEqual(0, len(self.dut))
