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

        # if cachepath doesnt exist, create it
        if not os.path.exists(self._path):
            try:
                os.makedirs(self._path)

            except OSError as e:

                if e.errno != errno.EEXIST:
                    raise e

    def __contains__(self, key):
        return self.path(key) in self.keys()

    def path(self, key):
        """
        convert key into a path.

        Subclasses may/should override to give appropriate extension to the
        filename
        """
        # normalize the key name
        # key = key.replace(os.sep, u'{0}{0}'.format(os.sep))

        # return the path to the object stored under key
        return unicode(os.path.join(self._path, key))

    def keys(self):
        """
        Return the set of keys in the backend.

        Keys are lazily generated on the first read, then cached.

        :return: the set of keys in the backend
        """

        if self._keys is None:
            self._keys = {f for f in os.listdir(self._path) if os.path.isfile(self.path(f))}

        return self._keys

    def delete(self, key):
        """
        Delete the item associated with key

        :param key: the path to delete
        :type key: str
        """
        assert isinstance(key, basestring), u'Key must be a string'

        try:

            path = self.path(key)

            # filesystem exit point, must manually handle utf-8 encoding
            os.remove(path)

            if self._keys is not None:
                self._keys.remove(path)

        except IOError as e:
            # item does not exist in the cache
            print e
            return True

        except OSError as e:
            # another error occurred
            print e
            return False

        else:
            return True

    def clear(self):
        """
        Remove all items from the cache

        :return:
        """
        for root, _, filenames in os.walk(self._path):
            for f in filenames:
                path = os.path.join(root, f)
                os.remove(path)

        self._keys = None

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
