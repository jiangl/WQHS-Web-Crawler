import urllib2
import sre
import sys
from time import clock, time
from datetime import date, datetime

#imports for musicbrainz
import logging
from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError


def load(address):
    try:
        web_handle = urllib2.urlopen(address)
        web_text = web_handle.read()
 #       matches = sre.findall('\<td class="pl"\>(.*?)\&', web_text)
 #       matches = sre.findall('\>(.*?)\&nbsp;\<', web_text)
        date_match = sre.findall('(\d{1,2}\-\d{1,2}\-\d{2})', web_text)

        lines = sre.findall('\<td class="plleft"\>(.*?)\</td\>\</tr\>', \
                            web_text)
            
        if (date_match != []):
            date = date_match[1];
            date = datetime.strptime(date, "%m-%d-%y")
            date = date.isocalendar()
            
            for line in lines:
                
                artist = ""
                song = ""
                album = ""

                matches = sre.findall('\<td class="pl"\>(.*?)\&nbsp', line)
                tracker = 1
                playlist = True
                
                for match in matches:
                    if tracker == 1:
                        artist = match
                        tracker = 2
                    elif tracker == 2:
                        song = match
                        tracker = 3
                    elif tracker == 3:
                        album = match
                        print "Artist: ", artist
                        print "Song: ", song
                        print "Album: ", album
                        print "Date: ", date
                        print
                        tracker = 4
                    elif tracker ==4:
                        tracker =1 
                    else:
                        print "Wtf this shouldn't happen."
        else:
            playlist = False
            pass
            print address

        return playlist
    
    except urllib2.HTTPError, e:
        print "Cannot retreieve URL: HTTP Error Code", e.code
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]


def lyrics(artist, song):
    try:
        address = 'http://www.azlyrics.com/lyrics/' + \
                  artist.replace(' ', '').lower() + '/' + \
                  song.replace(' ', '').lower() + '.html'
        web_handle = urllib2.urlopen(address)
        web_text = web_handle.read()
        lyrics = sre.findall('(?s)<!-- start of lyrics -->.*?<!', web_text, sre.MULTILINE)
        
        return lyrics
    except urllib2.HTTPError, e:
        print "Cannot retreieve URL: HTTP Error Code", e.code
    except urllib2.URLError, e:
        print "Cannot retrieve URL: " + e.reason[1]


if __name__ == "__main__":
##    #6425 total so far, 0.0125units = 1 second
    for page in range(6476,6477):
        load('http://www.wqhs.org/playlist.php?id='+ str(page))

##    words = lyrics('Carly Rae Jepsen', 'Call Me Maybe');
##    print words


