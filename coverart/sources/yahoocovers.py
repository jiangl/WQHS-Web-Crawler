import sys
import xml.etree.ElementTree as ET
from urllib import urlencode, urlopen
from httplib import HTTPConnection
from urlparse import urlparse
from coverart.sources import CoverSourceBase

def url_is_image(url): #{{{1
    u = urlparse(url)
    host = u.netloc
    port = u.port
    path = u.path
    if u.query:
        path += '?' + u.query
    try:
        conn = HTTPConnection(host, port)
        conn.request('HEAD', path)
        resp = conn.getresponse()
    except:
        return False
    content_type = resp.getheader('content-type')
    if content_type and content_type.startswith('image/'):
        return True
    return False

#}}}1

class CoverSource(CoverSourceBase): #{{{1

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.source_name = 'Yahoo!'
        self.appid = 'VRmspbXV34FFL7cFtXA0A901F6pU.QAXlG.tMPN7i3G2qc_8ShbS5SixFPkUlASWuw--'
        self.url_base = 'http://search.yahooapis.com'
        self.xmlns = 'urn:yahoo:srchmi'

    def search(self, query):
        p = {
                'appid': self.appid,
                'query': query,
                'results': self.max_results,
                }
        url = '%s/ImageSearchService/V1/imageSearch?%s' % (self.url_base, urlencode(p))
        ns = self.xmlns
        xml = ET.parse(urlopen(url)).getroot()
        count = 0
        for elem in xml.findall('{%s}Result' % self.xmlns):
            album = elem.find('{%s}Summary' % ns).text or 'Unknown'
            cover_large = elem.find('{%s}Url' % ns).text
            if url_is_image(cover_large):
                count += 1
                yield {
                        'album': album,
                        'cover_large': cover_large,
                        'cover_small': elem.find('{%s}Thumbnail/{%s}Url' % (ns, ns)).text,
                        }
                if count == self.max_results: break

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
