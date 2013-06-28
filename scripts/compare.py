#! /home/ubuntu/funnelweb/compare/bin/python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import re


site_url = 'http://sure.grafware.com'

pat = [
            (' (\d+)\.(\d+) ', r' \1,\2 '),
      ]
strs = [
            (u'Tip a friend', u'Sugg\xe9rer \xe0 un ami'),
            (u'Modified', u'Modifi\xe9'),
            (u'Latest News!', u'Derni\xe8res nouvelles !\n\n\nLisez r\xe9guli\xe8rement nos derni\xe8res nouvelles !\n\n\n\n\nSugg\xe9rer \xe0 un ami\n\n\n\n'),
            (u'Previous', u'Pr\xe9c\xe9dent'),
            (u'Next', u'Suivant'),
            (u'Read more', u'En savoir plus'),
      ]

import urllib2

def get_text(path):
    try:
        html = urllib2.urlopen(site_url + path).read()
    except urllib2.HTTPError:
        return ''
    soup = BeautifulSoup(html)
    try:
        d1 = soup.find_all('div', class_='content-view-full')[0]
    except IndexError:
        d1 = soup.find_all(id='maincontent-design')[0]
    return d1.text

def compare(url1, url2):
    t1 = get_text(url1)
    t2 = get_text(url2)
    for p in pat:
        t2 = re.sub(p[0], p[1], t2)
    for p in strs:
        t2 = t2.replace(p[0], p[1])
    if t1 != t2:
        #import pdb; pdb.set_trace()
        pass
    return t1 == t2, t1, t2

def file_compare(lang):
    f1 = '/home/ubuntu/funnelweb/batches/do.fr'
    f2 = '/home/ubuntu/funnelweb/batches/do.%s' % lang
    fp1 = open(f1)
    l1 = [x.strip() for x in fp1]
    fp1.close()
    fp1 = open(f2)
    l2 = [x.strip() for x in fp1]
    fp1.close()
    fp1 = open('unique_pinch.%s' % lang, 'w')
    fp2 = open('details_pinch.%s' % lang, 'w')
    for line in l2:
        if line.endswith('.pdf'):
            continue
        l_fr = line.replace('/%s/' % lang, '/fr/')
        if l_fr in l1:
            out = compare(l_fr, line)
            if out[0]:
                print >> fp1, 'SAME', line
            else:
                print >> fp1, 'DIFF', line
                print >> fp2, '++++++++++++++++++++', line
                print >> fp2, out[1].encode('utf-8')
                print >> fp2, '--------------------'
                print >> fp2, out[2].encode('utf-8')
        else:
            print >> fp1, 'UNIQ', line
    fp1.close()
    fp2.close()

file_compare('it')
