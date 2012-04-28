import urllib2
import sre
import sys
from time import clock, time

#imports for musicbrainz
import logging
from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError


def load(address):
    try:
        web_handle = urllib2.urlopen(address)
        web_text = web_handle.read()
        matches = sre.findall('\<td class="pl"\>(.*?)\&', web_text)
        date_match = sre.findall('(\d{1}\-\d{2}\-\d{2})', web_text)
        date = date_match[1];
        
        tracker = 1
        
        artist = ""
        song = ""
        album = ""
        
        for match in matches:
            if tracker == 1:
                artist = match
                tracker = 2
            elif tracker == 2:
                song = match
                tracker = 3
            elif tracker == 3:
                album = match
                #do dictionary shit here
##                print "Artist: ", artist
##                print "Song: ", song
##                print "Album: ", album
##                print "Date: ", date
##                print
                tracker = 1
            else:
                print "Wtf this shouldn't happen."
            
    except urllib2.HTTPError, e:
        print "Cannot retreieve URL: HTTP Error Code", e.code
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]

##def cover(album):
##    
        
if __name__ == "__main__":
    start = clock()
    #6425 total so far, 0.0125units = 1 second
    for page in range(2,3):
        load('http://www.wqhs.org/playlist.php?id='+ str(page))
    elapsed = (clock() - start)
    print elapsed

