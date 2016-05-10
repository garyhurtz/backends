# -*- coding: UTF-8 -*- #
from S3BaseBackend import S3BaseBackend
from boto.exception import S3ResponseError
from boto.s3.key import Key
import StringIO
import gzip


class S3RawBackend(S3BaseBackend):
    """
    Backend that stores raw files on S3.

    """
    # u'text/plain', u'text/csv', u'application/xml'
    COMPRESSIBLE = [u'application/javascript', u'text/css']

    def load(self, key):
        """
        Load key from the backend.

        :param key: the key for the object to load
        """

        if key is None:
            raise ValueError(u'Key cannot be None')

        k = Key(self.bucket)
        k.key = key

        try:
            data = k.get_contents_as_string()

        except S3ResponseError as e:
            # raised if the key cant be found
            return None

        except Exception as e:
            raise e
            return None

        else:
            return data

    def dump(self, key, fp, public=False, mimetype=None, cache=False):
        """
        Dump the uploaded file to S3

        if mimetype not set attempt to extract content_type from the file

        by default the file will be private, set public to make public
        :param key: the key to store the object under
        :param fp: filepointer
        :param public: whether the object should me made public
        :param mimetype: force the mimetype
        :param cache: cache-control header
        """

        k = Key(self.bucket)
        k.key = key

        headers = {}

        # set file permissions
        policy = u'public-read' if public else None

        try:

            # if mimetype not forced get from fp
            if mimetype is None and hasattr(fp, u'content_type'):
                mimetype = fp.content_type

            headers[u'Content-Type'] = mimetype

            if cache:
                # the value must be a byte string or else URL encoding goofs it up
                headers[u'Cache-Control'] = u'public, max-age={0}'.format(cache)

            if mimetype in self.COMPRESSIBLE:
                print u'compressing ', key
                headers[u'Content-Encoding'] = u'gzip'

                sio = StringIO.StringIO()
                gzf = gzip.GzipFile(fileobj=sio, mode='wb')
                gzf.write(fp.read())
                gzf.close()

                # Output gzipped stream.
                content = sio.getvalue()

            else:
                content = fp.read()

            k.set_contents_from_string(content, headers=headers, policy=policy)

        except Exception as e:
            raise e
            return False

        else:
            # now update the cache
            if self._keys is not None:
                self._keys.add(k.key)
            return True
