# -*- coding: UTF-8 -*- #

from datetime import datetime, timedelta
from VolatileBackend import VolatileBackend
from FileSystemJsonBackend import FileSystemJsonBackend


class JsonCache(object):
    """
    Cache items to the FileSystem in JSON format

    items are cached locally

    values stored in serialized format, in order to match the result of an sdb query

    if path is None, cache is volatile but provides a consistent interface
    """

    def __init__(self, path=None, timeout=300):

        assert isinstance(timeout, int), u'timeout must be an integer'

        self._timeout = timeout

        # cache retrieved items locally for faster response
        # key is string, value is dict or list
        self.locals = {}

        if path is None:
            self.backend = VolatileBackend()

        else:
            self.backend = FileSystemJsonBackend(path)

    def __iter__(self):
        return iter(self.backend)

    def __len__(self):
        return len(self.backend)

    def __contains__(self, key):
        return key in self.locals or key in self.backend

    def keys(self):
        return self.backend.keys()

    def items(self):
        return self.backend.items()

    def get(self, key):
        """
        Retrieve item from the cache

        If expired or doesnt exist return None, else return item
        """

        # if the item is already cached, return it
        if key not in self.locals:

            result = self.deserialize(self.backend.load(key))

            # item doesnt exist, return None
            if result is None:
                return None

            # item has expired, delete it and return none
            if datetime.utcnow() > result.get(u'expiration'):
                self.delete(key)
                return None

            # item is ok, cache the content locally and return it
            self.locals[key] = result.get(u'content')

        return self.locals[key]

    def set(self, key, value, timeout=None):
        """
        Cache a pre-serialized value
        """

        assert isinstance(key, basestring), u'Key must be a string'

        assert isinstance(value, dict) or isinstance(value, list), u'Value must be JSON serializable'

        # set the local cache
        self.locals[key] = value

        expiration = datetime.utcnow() + timedelta(seconds=(timeout or self._timeout))

        serialized = self.serialize(value, expiration)

        self.backend.dump(key, serialized)

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

    def deserialize(self, data):
        """
        Accepts the json-deserialized object, performs any additional deserialization, then returns it.
        """
        if data is None:
            return None

        # deserialize the expiration before returning
        data[u'expiration'] = datetime.strptime(data[u'expiration'], self.backend.time_format)
        return data

    def serialize(self, value, expiration):
        """
        Formats value for serialization.
        """
        return {
            u'expiration': datetime.strftime(expiration, self.backend.time_format),  # timestamp
            u'content': value
        }

    def prune(self):
        """
        Delete all expired items from the cache
        :return:
        """
        all_keys = {k for k in self.keys()}

        for key in all_keys:
            self.get(key)

    def clear(self):
        """
        Clear all items from the cache
        :return:
        """
        self.backend.clear()
