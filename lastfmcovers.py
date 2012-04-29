import sys
from coverart.sources import CoverSourceBase
from urllib import urlopen, quote_plus
from xml.etree.ElementTree import parse

class CoverSource(CoverSourceBase):

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.source_name = 'Last.FM'
        self.api_key = '2f63459bcb2578a277c5cf5ec4ca62f7'
        self.url_base = 'http://ws.audioscrobbler.com/2.0/?method=album.search&api_key=%s' % self.api_key

    def search(self, query):
        url = '%s&album=%s' % (self.url_base, quote_plus('%s' % query))
        tree = parse(urlopen(url))
        count = 0
        for a in tree.findall('results/albummatches/album'):
            result = {}
            if (a.findtext('name').lower() == query.lower()):
                for i in a.findall('image'):
                    size = i.get('size')
                    if size == 'extralarge':
                        result = i.text
                    elif (size == 'large') & (result == ''):
                        result = i.text
                count += 1
                return result
                if count == self.max_results:
                    break

if __name__ == '__main__':
    c = CoverSource()
    result = c.search('Is this it')
    print result
