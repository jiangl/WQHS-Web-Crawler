import sys
from urllib import urlopen, urlencode
from coverart.sources import CoverSourceBase
from xml.etree.ElementTree import parse

class CoverSource(CoverSourceBase): #{{{1

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.source_name = 'Amazon'
        self.url_base = 'http://free.apisigning.com/onca/xml'
        self.key = 'AKIAJVIEODBXLUUDP3VQ'
        self.xmlns = 'http://webservices.amazon.com/AWSECommerceService/2005-10-05'

    def search(self, query):
        p = {
                'Service': 'AWSECommerceService',
                'Operation': 'ItemSearch',
                'ContentType': 'text/xml',
                'AWSAccessKeyId': self.key,
                'SearchIndex': 'Music',
                'ResponseGroup': 'Images,Small',
                'Keywords': query,
                }
        tree = parse(urlopen('%s?%s' % (
            self.url_base, urlencode(p)))).getroot()
        count = 0
        for item in tree.findall('.//{%s}Item' % self.xmlns):
            result = {}
            result['album'] = item.findtext('.//{%s}Title' % (self.xmlns))
            result['cover_large'] = item.findtext('.//{%s}LargeImage/{%s}URL' % (self.xmlns, self.xmlns))
            result['cover_small'] = item.findtext('.//{%s}SmallImage/{%s}URL' % (self.xmlns, self.xmlns))
            if not result['cover_large']: continue
            if not result['cover_small']:
                result['cover_small'] = result['cover_large']
            if count == self.max_results: break
            count += 1
            yield result

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
