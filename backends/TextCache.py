# -*- coding: UTF-8 -*- #

import os
import time
from backends.VolatileBackend import VolatileBackend
from backends.FileSystemTextBackend import FileSystemTextBackend


class TextCache(object):
    """
    Cache text files to the FileSystem.

    Expiration is tested once per request, the first time the file is retrieved.
    After the first retrieval the value is stored in a dict.

    Expired files return None.

    If path is None use VolatileCache
    """

    def __init__(self, path=None, timeout=300):

        assert isinstance(timeout, int), u'timeout must be an integer'

        self._timeout = timeout

        # retrieved items are cached locally
        # expiration is tested the first time each file is retrieved during a request
        #
        # key is a string, value is a file
        self.locals = {}

        if path is None:
            self.backend = VolatileBackend()

        else:
            self.backend = FileSystemTextBackend(path)

    def __iter__(self):
        return iter(self.backend)

    def __len__(self):
        return len(self.backend)

    def __contains__(self, key):
        return key in self.backend

    def keys(self):
        return self.backend.keys()

    def items(self):
        return self.backend.items()

    def _file_expired(self, key):
        # get the file creation time

        file_age = time.time() - os.path.getctime(self.backend.path(key))
        expiration_msec = self._timeout * 1000

        return file_age > expiration_msec

    def get(self, key):
        """
        Retrieve item from the cache

        If expired or doesnt exist return None, else return item
        """

        # if the item is already cached, return it
        # items do not expire mid-request
        if key not in self.locals:

            if key not in self.backend:
                return None

            # key exists, so check expiration
            # if file expired, delete it and return None
            if self._file_expired(key):
                self.delete(key)
                return None

            self.locals[key] = self.backend.load(key)

        return self.locals[key]

    def set(self, key, value):
        """
        Cache a pre-serialized value
        """

        assert isinstance(key, basestring), u'Key must be a string'

        # local keys are paths
        self.locals[key] = value

        # backend dumps keys into subdirectories
        self.backend.dump(key, value)

    def delete(self, key):

        if key in self.locals:
            del self.locals[key]

        return self.backend.delete(key)

    def batch_delete(self, keys):
        """
        convenience method to provide a similar interface as boto

        keys is a dict containing keys of items to delete
        """
        for key in keys:
            self.delete(key)

    def prune(self):
        """
        Delete all expired items from the cache
        :return:
        """
        expired_keys = {k for k in self.keys() if self._file_expired(k)}

        for key in expired_keys:
            self.delete(key)

    def clear(self):
        """
        Clear all items from the cache
        :return:
        """
        self.backend.clear()
