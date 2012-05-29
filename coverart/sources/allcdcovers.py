import sys, re
from coverart.sources import CoverSourceBase
from urllib import urlopen, quote_plus

class CoverSource(CoverSourceBase): #{{{1

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.source_name = 'AllCDCovers'
        self.url_base = 'http://www.allcdcovers.com'

    def search(self, query):
        url = '%s/search/music/all/%s' % (self.url_base, quote_plus(query))
        results_page = urlopen(url).read()
        seen = set()
        count = 0
        for rm in re.finditer(r'<a href="(/show/.*?/.*?/front)">', results_page):
            if not rm or rm.group(1) in seen: continue
            cover_page = urlopen(self.url_base + rm.group(1)).read()
            clm = re.search(r'<a href="(/download/.*?)">', cover_page)
            csm = re.search(r'<div class="productImage"><img .*?src="(/image_system/.*?)" />', cover_page)
            am = re.search(r'<dt>Title:</dt><dd>(.*?)</dd>', cover_page)
            if am and csm and clm:
                count += 1
                yield {
                        'album': am.group(1),
                        'cover_large': self.url_base + clm.group(1),
                        'cover_small': self.url_base + clm.group(1),
                        }
            if count == self.max_results: break
            seen.add(rm.group(1))

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
