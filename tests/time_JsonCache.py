from datetime import datetime
from backends.JsonCache import JsonCache
from werkzeug.contrib.cache import FileSystemCache
from tests import cachepath

from random import shuffle

lc = JsonCache(None)
fsc = FileSystemCache(cachepath)
jc = JsonCache(cachepath)

results = dict()

duts = [('lc', lc), ('fsc', fsc), ('jc', jc)]

for i in range(100):
    shuffle(duts)

    for tag, cache in duts:

        if tag not in results:
            results[tag] = []

        start = datetime.utcnow()

        cache.set('blah', 'blahblah')
        cache.get('blah')
        cache.set('blah1', 'blahblah')
        cache.get('blah1')
        cache.set('blah2', 'blahblah')
        cache.get('blah2')
        cache.set('blah3', 'blahblah')
        cache.get('blah3')
        cache.set('blah4', 'blahblah')
        cache.get('blah4')
        cache.set('blah5', 'blahblah')
        cache.get('blah5')

        results[tag].append((datetime.utcnow() - start).microseconds)

print '{0:10}{1:10}{2:10}{3:10}'.format('tag', 'min', 'max', 'ave')
for tag, cache in duts:
    print '{0:10}{1:10}{2:10}{3:10}'.format(tag, min(results[tag]), max(results[tag]), sum(results[tag])/len(results[tag]))
