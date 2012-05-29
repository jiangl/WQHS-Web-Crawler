import sys, re
from coverart.sources import CoverSourceBase
from urllib import urlopen, quote_plus

class CoverSource(CoverSourceBase): #{{{1

    def __init__(self):
        CoverSourceBase.__init__(self)
        self.source_name = 'Discogs'
        self.url_base = 'http://www.discogs.com'

    def search(self, query):
        url = '%s/search?type=releases&q=%s' % (self.url_base, quote_plus('"%s"' % query))
        results_page = urlopen(url).read()
        count = 0
        for rm in re.finditer(r'<li class="search_result">.*?<a href="(.*?)">', results_page, re.DOTALL):
            cover_page = urlopen(self.url_base + rm.group(1)).read()
            tm = re.search(r'<title>(.*?) at Discogs</title>', cover_page)
            im = re.search(r'<a href="(/viewimages\?release=.*?)">', cover_page)
            if not im: continue
            images_page = urlopen(self.url_base + im.group(1)).read()
            im = re.search(r'<img src="(.*?/image/.*?)"', images_page)
            if not im: continue
            count += 1
            yield {
                    'album': tm.group(1) if tm else 'N/A',
                    'cover_large': im.group(1),
                    'cover_small': im.group(1),
                    }
            if count == self.max_results:
                break

#}}}1

if __name__ == '__main__':
    c = CoverSource()
    for result in c.search(sys.argv[1]):
        print result
