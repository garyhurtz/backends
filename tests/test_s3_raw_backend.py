# -*- coding: UTF-8 -*- #
import unittest
from backends.S3RawBackend import S3RawBackend


class TestS3Basic(unittest.TestCase):

    def setUp(self):
        self.dut = S3RawBackend(u'test-stellour')

        with open(u'main.css', u'r') as infile:
            self.dut.dump(u'test', infile)

    def tearDown(self):
        self.dut.clear()

    def test_lump(self):
        """
        Since it takes time to upload and clear the object for each
        test, just do all the basics in one run

        :param key:
        :return:
        """
        self.assertTrue(u'test' in self.dut)
        self.assertTrue(u'test' in self.dut.keys())
        self.assertIsInstance(self.dut.load(u'test'), basestring)

        before = len(self.dut)
        self.assertTrue(self.dut.delete(u'test'))
        self.assertEqual(1, before - len(self.dut))


class TestS3RawBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dut = S3RawBackend(u'test-stellour')

    @classmethod
    def tearDownClass(cls):
        cls.dut.clear()

    def execute(self, key, original):

        before = len(self.dut)
        result = self.dut.dump(key, original)

        self.assertTrue(result)
        self.assertEqual(1, len(self.dut) - before)

        # confirm no errors on load
        self.dut.load(key)

    @unittest.expectedFailure
    def test_is_gzipped(self):
        """
        Need a clean way to confirm that the file was gzipped
        :return:
        """
        raise NotImplementedError()

    def test_dump_css_fp(self):
        """
        Store a value in the backend
        """
        key = u'css_fp'

        with open(u'main.css', u'r') as value:
            self.execute(key, value)

    def test_dump_css_string(self):
        """
        Store a value in the backend
        """
        key = u'css_string'

        with open(u'main.css', u'r') as infile:
            value = infile.read()

        self.execute(key, value)

    def test_dump_png_fp(self):
        """
        Store a value in the backend
        """
        key = u'png_fp'

        with open(u'test.png', u'r') as value:
            self.execute(key, value)

    def test_dump_png_as_string(self):
        """
        Store a value in the backend
        """
        key = u'png_string'

        with open(u'test.png', u'r') as infile:
            value = infile.read()

        self.execute(key, value)

    def test_dump_ascii_string(self):
        """
        Store a value in the backend
        """
        key = u'ascii'
        value = 'this is a test string'

        self.execute(key, value)

    def test_dump_unicode_string(self):
        """
        Store a value in the backend
        """
        key = u'中文'
        value = u'一点点中文'

        self.execute(key, value)

