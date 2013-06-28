#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import urllib2, socket, sys
from urlparse import urlparse
from collections import Counter

SRC_URL = 'http://sure.grafware.com'
URL1 = '/en/content/download/2072/23116/file/GdP-Animation%20Journée%20de%20la%20Paix-06.pdf'

FILE_TYPES = ('application/pdf',)

DEST_URL = 'http://test.g2p.webfactional.com'

def do_all():
    fp = urllib2.urlopen(SRC_URL + URL1)
    info = fp.info()
    if info.get('Content-Type', None) in FILE_TYPES:
        content = fp.read()
        print info['Content-Length'], len(content)
    else:
        print 'Not a file'

do_all()
