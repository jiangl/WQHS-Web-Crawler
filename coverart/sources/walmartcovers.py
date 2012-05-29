import sys, re
from urllib import urlopen, urlencode
from coverart.sources import CoverSourceBase

class CoverSource(CoverSourceBase): #{{{1

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.url_base = 'http://www.walmart.com'
        self.source_name = 'Walmart'

    def search(self, query):
        p = {
                'search_query': query,
                'search_constraint': 4104,
                'ic': str(self.max_results)+'_0'
                }
        check_current_page = True
        results_page = urlopen('%s/search/search-ng.do?%s' % (
            self.url_base, urlencode(p))).read()
        for rm in re.finditer(r'<a href="/(catalog/product\.do\?product_id=.*?)">(.*?)</a>', results_page):
            check_current_page = False
            album_page = urlopen('%s/%s' % (self.url_base, rm.group(1))).read()
            result = self.parse_album_page(album_page)
            if result: yield result
        if check_current_page:
            am = re.search(r'<title>Walmart\.com: (.*?): [^:]+</title>', results_page)
            cm = re.search(r'''<a href=".*?'(.*?)&.*<img.*?src='(.*?)'.*?</a>''', results_page)
            if am and cm:
                yield {
                        'album': am.group(1),
                        'cover_large': cm.group(1),
                        'cover_small': cm.group(2)
                        }

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
