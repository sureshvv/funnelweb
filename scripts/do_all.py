#!/usr/bin/python -u

import httplib, socket, sys
from urlparse import urlparse
from collections import Counter

SRC_URL = 'http://sure.grafware.com'
DEST_URL = 'http://test.g2p.webfactional.com'

skip_ids = ( '/tipafriend/',
           )

map_ids = ( 
            ('/view',                      '/view-1'),
            ('/layout',                    '/layout-1'),
            ('/edit',                      '/edit-1'),
            ('%C3%A7',                     'c'),
            ('%C3%A0',                     'a'),
            ('%C3%A8',                     'e'),
            ('%C3%A9',                     'e'),
            ('%C3%B4',                     'o'),
            ('%CC%8',                      '30'),
            ("%5C'",                       '-'),
            ('%20.',                       '.'),
            ('%20',                        '-'),
          )



done = {}

def checkUrl(url, prefix=None):
    if prefix:
        url = prefix + url
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

def do_all(infile, from_wget):
    with open(infile) as fp:
        for url in fp:
            url = url.strip()
            if url.endswith('.css'):
                continue
            if any([s for s in skip_ids if s in url]):
                continue
            if url in done:
                continue
            url = url.rstrip('%20')
            orig_url = url
            for i,j in map_ids:
                url = url.replace(i, j)
            while url.find('--') >= 0:
                url = url.replace('--', '-')
            try:
                rc = checkUrl(url, DEST_URL)
            except socket.gaierror:
                done[orig_url] = 'Elocal'
                continue
            if rc:
                done[orig_url] = 'OK'
                continue
            if from_wget:
                try:
                    rc = checkUrl(orig_url, SRC_URL)
                except socket.gaierror:
                    done[orig_url] = 'Eremote'
                    continue
                if not rc:
                    done[orig_url] = '404'
                    continue
            done[orig_url] = 'TODO'
            print done[orig_url], orig_url
    rc = Counter(done.values())
    print rc.items()

def do_url(infile):
    with open(infile) as fp:
        for url in fp:
            try:
                rc = checkUrl(url)
            except socket.gaierror:
                status = 'ERR',
            else:
                status = 'OK' if rc else '404'
            print status, url

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1] == "-2":
            do_all(sys.argv[2], True)
            sys.exit(0)
        elif sys.argv[1] == "-1":
            do_url(sys.argv[2])
            sys.exit(0)
    print "Usage: do_all.py -1|-2 <infile>"
    sys.exit(-1)
