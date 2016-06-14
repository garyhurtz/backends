# -*- coding: UTF-8 -*- #

from BaseBackend import BaseBackend


class VolatileBackend(BaseBackend):
    """
    Backend that stores values in a dictionary.

    Primarily for testing.
    """

    def __init__(self):
        BaseBackend.__init__(self)
        self.data = dict()

    def keys(self):
        return {key for key in self.data.keys()}

    def load(self, key):
        return self.data.get(key, None)

    def dump(self, key, value):
        self.data[key] = value
        return True

    def delete(self, key):
        return self.data.pop(key)

    def clear(self):
        return self.data.clear()
