# -*- coding: UTF-8 -*- #
import abc


class BaseBackend(object):
    """
    Backend interface.

    Each subclass must implement keys, items, load, dump, etc.

    Note: keys is the master method, other functions derived from keys
    """

    # unified time format
    _time_format = u'%Y-%m-%dT%H:%M:%S'

    @property
    def time_format(self):
        return self._time_format

    def __len__(self):
        """
        :return: Return the number of values in the backend
        """
        return len(self.keys())

    def __contains__(self, key):
        """
        :param key: the name of the key to test
        :return: Return True if key is in the backend, else False
        """
        return key in self.keys()

    def __iter__(self):
        """
        :return: An iterator containing *key, value) pairs for all items in the backend
        """
        return iter(self.keys())

    def items(self):
        """
        :return: A generator containing (key, value) pairs for all items in the backend
        """
        return ((key, self.load(key)) for key in self.keys())

    def clear(self):
        """
        Generic clear method.

        Override when better implementations are available.

        :return:
        """
        keys = [k for k in self.keys()]

        for k in keys:
            self.delete(k)

    @abc.abstractmethod
    def keys(self):
        """
        :return: The set of keys in the backend
        """
        return {}

    @abc.abstractmethod
    def load(self, key):
        """
        :param: key
        :return: The value stored under key
        """
        pass

    @abc.abstractmethod
    def dump(self, key, value):
        """
        :param: key, the key to store the value under
        :param: value, the value
        :return: True if the dump was successful, else False
        """
        pass

    @abc.abstractmethod
    def delete(self, key):
        """
        Delete a value from the backend
        :param: key
        :return: True if the delete was successful, else False
        """
        pass
