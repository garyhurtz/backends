# -*- coding: UTF-8 -*- #

from FileSystemBaseBackend import FileSystemBaseBackend
import os
import codecs
import errno


class FileSystemTextBackend(FileSystemBaseBackend):
    """
    Backend that stores values on the filesystem.

    Values are stored in text files, values are returned as unicode (utf-8) strings

    """

    def load(self, key):

        assert isinstance(key, basestring), u'Key must be a string'

        filename = self.path(key)

        try:
            with codecs.open(filename, u'r', u'utf-8') as f:
                # filesystem entry point, must manually encode
                data = f.read()

        except IOError:
            # Raised if the file cant be opened
            return None

        except OSError:
            # Raised if there is an OS-related error
            return None

        else:
            return data

    def dump(self, key, value):
        """

        :param key: the key to store the value under
        :param value: a string or file pointer, stringifies all other types
        :return:
        """

        assert isinstance(key, basestring), u'Key must be a string'

        # if value is a file, read it into a string
        if isinstance(value, file):
            value = value.read()

        # if value is not already a string, convert it to unicode
        if not isinstance(value, basestring):
            value = unicode(value)

        try:

            # now update the cache
            path = self.path(key)
            dirname = os.path.dirname(path)

            if self._keys is None:
                self._keys = set()

            self._keys.add(path)

            # create the cache directory that will hold the template, if needed
            if not os.path.exists(dirname):

                try:
                    os.makedirs(dirname)

                except OSError as e:

                    if e.errno != errno.EEXIST:
                        raise e

            with codecs.open(path, u'w', u'utf-8') as outfile:
                outfile.write(value.decode(u'utf-8'))

        except IOError as e:
            print e
            return False

        except OSError as e:
            print e
            return False

        else:
            return True
