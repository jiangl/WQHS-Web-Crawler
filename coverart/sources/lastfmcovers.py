import sys
from coverart.sources import CoverSourceBase
from urllib import urlopen, quote_plus
from xml.etree.ElementTree import parse

class CoverSource(CoverSourceBase): #{{{1

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
            result['album'] = a.findtext('name')
            for i in a.findall('image'):
                size = i.get('size')
                if size == 'extralarge':
                    result['cover_large'] = i.text
                elif size == 'large':
                    result['cover_small'] = i.text
            if 'cover_large' not in result: continue
            if 'cover_small' not in result:
                result['cover_small'] = result['cover_large']
            count += 1
            yield result
            if count == self.max_results:
                break

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
