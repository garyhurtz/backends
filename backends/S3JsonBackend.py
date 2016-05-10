# -*- coding: UTF-8 -*- #
from S3BaseBackend import S3BaseBackend
from boto.exception import S3ResponseError
from boto.s3.key import Key
import json

__author__ = 'gary'


class S3JsonBackend(S3BaseBackend):
    """
    Backend that stores values on S3.

    Values must be json-serializable (i.e. dicts or lists)
    """

    def load(self, key):
        """
        Load key from the backend.

        """

        assert isinstance(key, basestring), u'Key must be a string'

        k = Key(self.bucket)
        k.key = key

        try:
            data = json.loads(k.get_contents_as_string(), encoding=u'utf-8')

        except S3ResponseError as e:
            # raised if the key cant be found
            return None

        except Exception as e:
            print e
            return None

        else:
            return data

    def dump(self, key, value, public=False):
        """
        Dump file to S3.

        Optionally make public
        """

        assert isinstance(key, basestring), u'Key must be a string'

        k = Key(self.bucket)
        k.key = key

        try:
            k.set_metadata(u'Content-Type', u'application/json')
            k.set_contents_from_string(json.dumps(value, sort_keys=True, indent=4, separators=(u',', u': ')))

            # set file permissions
            if public:
                k.set_acl(u'public-read')

        except Exception as e:
            print e
            return False

        else:
            # now update the cache
            if self._keys is not None:
                self._keys.add(key)
            return True
