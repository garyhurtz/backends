# -*- coding: UTF-8 -*- #
from BaseBackend import BaseBackend
import abc
from boto import connect_s3
from boto.s3 import connect_to_region
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat


class S3BaseBackend(BaseBackend):
    """
    Base class for storing objects on S3

    All S3 functions are implemented here, with formats, etc implemented in subclasses

    AWS credentials should be supplied per boto, generally by setting
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
    """

    def __init__(self, bucket, region=u'ap-southeast-1'):

        BaseBackend.__init__(self)
        self._bucketname = bucket
        self.region = region
        self._s3_connection = None
        self._bucket = None
        self._keys = None

    def __contains__(self, key):
        """
        :param key:
        :return: True if the backends contains key, else False
        """
        return self.bucket.get_key(key) is not None

    def url(self, bucket, key):
        """
        Return the url to the object stored under key

        :param bucket: the name of the bucket
        :param key: the key
        :return: the url
        """
        return u'http://{0}.s3.amazonaws.com/{1}'.format(bucket, key)

    def make_public(self, key):
        """
        Make the object stored under key public
        """
        assert isinstance(key, basestring), u'Key must be a string'

        k = Key(self.bucket)
        k.key = key
        k.set_acl(u'public-read')

    def make_private(self, key):
        """
        Make the object stored under key private
        """
        assert isinstance(key, basestring), u'Key must be a string'

        k = Key(self.bucket)
        k.key = key
        k.set_acl(u'private')

    @property
    def connection(self):
        """
        Lazy connection to S3.
        """

        if self._s3_connection is None:

            if self.region:
                self._s3_connection = connect_to_region(
                    self.region,
                    is_secure=True,
                    calling_format=OrdinaryCallingFormat()
                )

            else:
                self._s3_connection = connect_s3()

        return self._s3_connection

    @property
    def bucket(self):
        """
        Lazy connection to bucket (via lazy connection)
        """
        if self._bucket is None:
            self._bucket = self.connection.get_bucket(self._bucketname, validate=False)

        return self._bucket

    def keys(self, folder=None):
        """
        Return the set of all keys in bucket.

        Caches results so you dont hit S3 too many times.

        :param folder: optional, limit results to those contained in folder
        """

        if self._keys is None:
            resultset = self.bucket.get_all_keys(prefix=folder)
            self._keys = {key.key for key in resultset}

        return self._keys

    def delete(self, key):
        """
        Delete item

        :param key:
        """
        assert isinstance(key, basestring), u'Key must be a string'

        try:
            self.bucket.delete_key(key)

        except Exception as e:
            return False

        else:
            # now update the cache
            if self._keys is not None:
                self._keys.remove(key)

            return True

    @abc.abstractmethod
    def load(self, key):
        """
        Retrieve a value from the backend

        Implement in subclass

        :param key:
        """
        pass

    @abc.abstractmethod
    def dump(self, key, value):
        """
        Store a value in the backend

        Implement in subclass

        :param key:
        :param value:
        """
        pass
