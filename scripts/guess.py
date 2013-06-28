#! /home/ubuntu/funnelweb/compare/bin/python -u

from guess_language import guessLanguage
import urllib2, sys

from bs4 import BeautifulSoup

site_url = 'http://sure.grafware.com'

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

def file_compare(infile):
    with open(infile) as fp:
        for line in fp:
            line = line.strip()
            lang = get_text(line)
            lang = guessLanguage(lang)
            print line, lang


file_compare(sys.argv[1])

