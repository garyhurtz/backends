# -*- coding: UTF-8 -*- #
import os

print str, os.listdir('tests/cache')
print str, [f.decode(u'utf-8') for f in os.listdir('tests/cache')]
print
print unicode, os.listdir(u'tests/cache')
print unicode, [f.encode(u'utf-8') for f in os.listdir(u'tests/cache')]
