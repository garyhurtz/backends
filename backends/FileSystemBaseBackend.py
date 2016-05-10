# -*- coding: UTF-8 -*- #
from BaseBackend import BaseBackend
import abc
import os
import errno


class FileSystemBaseBackend(BaseBackend):
    """
    Base backend for storing files on the filesystem

    Subclasses must override load() and dump() methods.
    """

    def __init__(self, path):
        BaseBackend.__init__(self)
        self._path = path

        self._keys = None

        if not os.path.exists(self._path):
            try:
                os.makedirs(self._path)

            except OSError as e:

                if e.errno != errno.EEXIST:
                    raise e

    def path(self, key):
        """
        convert key into filename and utf-8 encode the result

        Subclasses may/should override to give appropriate extension to the
        filename
        """
        return os.path.join(self._path, key).encode(u'utf-8')

    @staticmethod
    def _strip_suffix(filename):
        """
        By default, values are cached on the filesystem as <key>, but
        subclasses may override path() to cache values as <key>.<suffix>.

        Strip the suffix if it exists, and return the key

        :param key:
        :return:
        """
        return filename.split(u'.')[0]

    def keys(self):
        """
        Return the set of keys in the backend.

        Keys are lazily generated on the first read, then cached.

        :return: the set of keys in the backend
        """

        if self._keys is None:
            self._keys = {self._strip_suffix(filename) for filename in os.listdir(self._path)}

        return self._keys

    def delete(self, key):
        """
        Delete the item associated with key

        :param key: the key to delete
        :type key: str
        """
        assert isinstance(key, basestring), u'Key must be a string'

        try:
            # filesystem exit point, must manually handle utf-8 encoding
            os.remove(self.path(key))

            # remove key from _keys, if needed
            if self._keys is not None:
                self._keys.remove(key)

        except IOError:
            # item does not exist in the cache
            return True

        except OSError as e:
            # another error occurred
            print e
            return False

        else:
            return True

    @abc.abstractmethod
    def load(self, key):
        """
        Retrieve a value from the backend

        Stub, override in the subclass
        """
        pass

    @abc.abstractmethod
    def dump(self, key, value):
        """
        Store a value in the backend

        Stub, override in the subclass
        """
        pass
