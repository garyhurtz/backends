# -*- coding: UTF-8 -*- #
import os

# provide a single cache location for tests to use
# tests need to clean up after themselves
cachepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), u'cache')

if not os.path.exists(cachepath):
    os.makedirs(cachepath)
