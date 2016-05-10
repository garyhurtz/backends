# -*- coding: UTF-8 -*- #


class BackendTests(object):

    def test_len(self):
        """
        Return the number of values in the backend
        :return:
        """
        self.assertEqual(1, len(self.dut))

    def test_iter(self):
        """
        Dict like retrieval of all items in the backend

        Equivalent to items()
        :return:
        """
        self.assertTrue(hasattr(iter(self.dut), u'__iter__'))

    def test_items(self):
        """
        Dict-like retrieval of all items in the backend.

        Items returned as an iterator.
        """
        self.assertEqual(1, len([i for i in self.dut.items()]))
