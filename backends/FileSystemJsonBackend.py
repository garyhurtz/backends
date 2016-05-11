# -*- coding: UTF-8 -*- #

from FileSystemBaseBackend import FileSystemBaseBackend
from flask import json
import os
import errno


class FileSystemJsonBackend(FileSystemBaseBackend):
    """
    Backend that stores JSON-serializable values on the filesystem.

    Automatically utf-8 encodes and decodes values at the filesystem entry/exit points.
    """

    def load(self, key):
        """
        Retrieve key from the backend, and deserialize the associated value into a Python object.

        :param key:
        :return:
        """

        assert isinstance(key, basestring), u'Key must be a string'

        filename = self.path(key)

        try:
            with open(filename) as f:
                # filesystem entry point, must manually encode
                data = json.load(f, encoding=u'utf-8')

        except ValueError as e:
            # ValueError is a superclass of JSONDecodeError and may catch other errors too
            # Raised if something is wrong with the JSON
            self.delete(key)
            print e, key
            return None

        except IOError as e:
            # Raised if the file cant be opened
            print e, key
            return None

        except OSError as e:
            # Raised if there is an OS-related error
            print e, key
            return None

        else:
            return data

    def dump(self, key, value):
        """
        Serialize JSON-formatted value to the filesystem

        :param key:
        :param value:
        :return:
        """
        assert isinstance(key, basestring), u'Key must be a string'

        try:

            path = self.path(key)
            dirname = os.path.dirname(path)

            if self._keys is None:
                self._keys = set()

            self._keys.add(path)

            if not os.path.exists(dirname):

                try:
                    os.makedirs(dirname)

                except OSError as e:

                    if e.errno != errno.EEXIST:
                        raise e

            with open(path, u'w') as outfile:
                json.dump(
                    value,
                    outfile,
                    encoding=u'utf-8',
                    sort_keys=True,
                    indent=4,
                    separators=(u',', u': ')
                )

        except IOError as e:
            print e, key
            return False

        except OSError as e:
            print e, key
            return False

        else:
            return True
