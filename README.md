# backends

General-purpose abstractions for various backends.

## BaseBackend

Defines the common interface for backends. The interface is generally a subset of the Python dict interface, plus *load* and *dump* methods which follow the json interface.

* *len(backend)* - the number of items in the backend
* *backend.keys()* - the set of keys in the backend
* *backend.items()* - a generator of key: value pairs in the backend
* *backend.load(key)* - load an item from the backend, or None if it doesnt exist.
* *backend.dump(key, value)* - dump an item to the backend. Return True if successful, else False.
* *backend.delete(key)* - delete an item from the backend. Return True if successful, else False.
* iter(backend) - return an iterator over backend.items()

backends also support the *in* operator:

for key in backend:
    ...
    
if key in backend:
    ...
    
## VolatileBackend
The VolatileBackend is a backend that stores values in memory, in a Python dictionary. Supports the common backend interface.

## FileSystem Backends
FileSystemBackends handle the logistics for connecting, saving, and retrieving data to/from the local filesystem. Unicode conversions are explicitly handled to overcome encoding variations between local development servers and AWS EC2 defaults.

The FileSystemBaseBackend is the superclass for FileSystem backends. This class is instantiated with the path to the cache folder, then handles key conversions as needed to load/dump values from/to the cache folder.

### FileSystemTextBackend
A backend that stores Unicode strings on the FileSystem.

### FileSystemJsonBackend
A backend that stores Python *dicts* or *lists* on the FileSystem in JSON format.

## S3 Backends
S3Backends handle the logistics for connecting, saving, and retrieving data to/from S3 buckets.

The S3BaseBackend is the superclass for S3 backends. This class is instantiated with the bucket name and region, then handles key conversions as needed to load/dump values from/to that bucket.

In addition to the common interface, S3 Backends have a few extra methods

* *url(bucket, key)* - return the url that can be used to access the object *key* within *bucket*. The object has to set public for this url to work.

* *make_public(key)* - make the object *key* public
* *make_private(key)* - make the object *key* private

AWS credentials should not be hard-coded into your code, and S3Backends support credentials as described [here](https://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs)

### S3JsonBackend
A backend that stores Python *dicts* or *lists* in an S3 bucket, in JSON format

### S3RawBackend
A backend that stores generic files in an S3 bucket.

If the file is javascript or css, it will be gzipped when upload to S3. Also supports setting cache-control headers.

## Caches
Caches apply the FileSystem backends to provide simple FileSystem caches, which can be used (for example) in conjunction with the S3Backends to cache objects retrieved from S3 to the local FileSystem.

### JsonCache
The JsonCache is essentially a FileSystemJsonBackend with an additional *timeout* parameter. When objects are dumped to the FileSystem, they are wrapped in an extra dictionary which stores the expiration time of the object:

When an object is retrieved from the cache one of the following happens:

* key is not in cache - return None
* key is in cache, expiration has passed - delete item from cache and return None
* key is in cache, expiration has not passed - deserialize and return the Python object

When the JsonCache is instantiated the default timeout is set, although this can be overridden on an object-by-object basis when the object is dumped into the cache.

### TextCache
The TextCache is essentially a FileSystemTextBackend with object expirations.

When an object is retrieved from the cache one of the following happens:

* key is not in cache - return None
* key is in cache, expiration has passed - delete item from cache and return None
* key is in cache, expiration has not passed - deserialize and return the Unicode string

Unicode strings are stored as-defined, and cache expiration is implemented by accessing the file age.
Unlike the JsonCache, per-object expiration is not supported.
