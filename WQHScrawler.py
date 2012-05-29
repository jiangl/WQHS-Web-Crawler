#!/usr/bin/python
'Provides functions to add songs from WQHS.org to music database (stored as nested dictionary) \
and to lookup information about most frequently played things on the radio'

import urllib2
import sre
import sys
import time
from datetime import date, datetime
from ast import literal_eval

from coverart.sources import CoverSourceBase 
from urllib import urlopen, quote_plus
from xml.etree.ElementTree import parse

import cgitb # for printing out to the web
cgitb.enable()


class WQHS(CoverSourceBase):
    'Crawler Class'

    def __init__(self):
        'Stores database, last page parsed, and coverart class'
        
        try:    
            load_data = open('WQHSdata.txt', 'rU')   # load dictionary      
            self.data = literal_eval(load_data.read())
            load_data.close()
        except IOError: # if file not found, make it
            self.data = {}           
            save = open('WQHSdata.txt', 'w')
            save.write(str(self.data))
            save.close()
            
        try:                                  
            load_last = open('last_page.txt', 'rU')   # load last page parsed
            self.last_page = eval(load_last.read())
            load_last.close()                     
        except IOError: # if file not found, or first time running, make it
            self.last_page = '2'
            save = open('last_page.txt', 'w')
            save.write(self.last_page)
            save.close()
        
        self.today = date.today()
        self.today = self.today.isocalendar()

        CoverSourceBase.__init__(self)
        self.source_name = 'Last.FM'
        self.api_key = '2f63459bcb2578a277c5cf5ec4ca62f7'
        self.url_base = 'http://ws.audioscrobbler.com/2.0/?method=album.search&api_key=%s' % self.api_key

        #sample data
##        self.data = {'the beatles': {'the white album': {'revolution': [(2012, 15, 7), (2012, 1, 7)],\
##                                                         'song 1'    : [(2011, 15, 4)]},
##                                     'let it be'      : {'let it be' : [(2011, 15, 1), (2011, 2, 3)], \
##                                                         'song 1'    : [(2012, 15, 3), (2009, 2, 2)]}},
##                     'lcd soundsystem':{'sound of silver':{'all my friends': [(2008, 17, 3), (2008, 17, 3), (2011, 17, 3)]}}}


                                           
    def lookup_artist(self, artist):
        'Enter name of artist to see how many songs by them were played'
        
        count = 0
        artist = artist.title()
        try:
            for albums in self.data[artist].values():
                for songs in albums.values():
                    count += len(songs)
        except KeyError:
            return 'Artist not found'
        
        output = '%d Songs Played By %s' % (count, artist)
        return output


        
    def timespan_select(self, timespan):
        'Enter timespan to see top played artist, album, and song in that timespan \
        possible arugments for timespan = last year, last month, last week, all time, or custom'

        'if custom is chosen, format is a tuple (start date, end date)\
        where the start date is the later date, and the end date is the more recent date '

        self.update()   # before looking up, update database
        end = self.today
        
        if timespan == 'last year':
            start = (self.today[0]-1, self.today[1], self.today[2]) # minus a year from today
        elif timespan == 'last month':
            start = (self.today[0], self.today[1]-4, self.today[2]) # minus 4 weeks from today
        elif timespan == 'last week':
            start = (self.today[0], self.today[1]-1, self.today[2]) # minus 1 week from today
        elif timespan == 'all time':
            start = (2006, 1, 1)                                                  
        elif isinstance(timespan, tuple): # if custom date range is passed in as tuple
            start = timespan[0]
            end = timespan[1]
        
        return self.lookup_freq(start, end, timespan) # call the lookup_freq function with specified timespan


    def lookup_freq(self, start, end, timespan):
        'Method by timespan_select to look through database'

        top_artist = [0]
        top_album  = [0]
        top_song   = [0]
        
        for artist in self.data.keys():
            artist_count = 0 # reset temp count for number songs in each album for artist
            
            for album in self.data[artist].keys():
                album_count = 0 # reset temp count for number songs in each list of dates

                for song in self.data[artist][album].keys():
                    song_count = 0 # reset temp count for number songs in each list of dates
                    
                    for date in self.data[artist][album][song]: 
                        if date >= start and date <= end and artist != '' and song != '':
                            # check ranges of dates (most inner loop) and for empty strings
                            if album != '':
                                song_count += 1
                                album_count += 1
                            artist_count += 1
                            
                    if song_count > top_song[0]: # after iterating through dates check if song beats the top spot
                        top_song   = [song_count, song, artist, album]
               
                if album_count > top_album[0]: # after iterating songs check if album beats the top spot
                    top_album = [album_count, album, artist]

            if artist_count > top_artist[0]: # after iterating through albums check if artist beats the top spot
                top_artist = [artist_count, artist]

        
        artist_result = 'Most played artist of %s is: %s (%s times)' % (timespan, top_artist[1], top_artist[0])
        album_result = 'Most played album  of %s is: %s, by %s (%s times)'  % (timespan, top_album[1], top_album[2], top_album[0])
        song_result = 'Most played song   of %s is: %s, by %s, off of the album %s (%s times)' % (timespan, top_song[1], top_song[2], top_song[3], top_song[0])

        top_album_art = self.cover_art(top_album[1])
        top_song_album_art = self.cover_art(top_song[3])
        top_song_lyrics = self.lyrics(top_song[2], top_song[1])

        return artist_result, album_result, song_result, top_album_art, top_song_album_art, top_song_lyrics
        
    
    def add_song(self, artist, song, album, date):
        'Enter name of artist, album, and song to add it to database'

        artist = artist.title()
        album = album.title()
        song = song.title()

        if artist not in self.data:
            self.data[artist] = {}
            self.data[artist][album] = {}
            self.data[artist][album][song] = [date]
            
        elif album not in self.data[artist].keys():
            self.data[artist][album] = {}
            self.data[artist][album][song] = [date]
            
        elif song not in self.data[artist][album].keys():
            self.data[artist][album][song] = [date]
            
        else:
            self.data[artist][album][song].append(date)
            
            
    def load(self, address):
        'Parse through webpages to find info'
        try:
            web_handle = urllib2.urlopen(address)
            web_text = web_handle.read()
            date_match = sre.findall('(\d{1,2}\-\d{1,2}\-\d{2})', web_text)

            lines = sre.findall('\<td class="plleft"\>(.*?)\</td\>\</tr\>', \
                                web_text)
            
                
            if (date_match != []):
                playlist = True
                date = date_match[1];
                date = datetime.strptime(date, "%m-%d-%y")
                date = date.isocalendar()
                
                for line in lines:
                    
                    artist = ""
                    song = ""
                    album = ""

                    matches = sre.findall('\<td class="pl"\>(.*?)\&nbsp', line)
                    tracker = 1
                    
                    for match in matches:
                        if tracker == 1:
                            artist = match
                            tracker = 2
                        elif tracker == 2:
                            song = match
                            tracker = 3
                        elif tracker == 3:
                            album = match
                            self.add_song(artist, song, album, date)
                            tracker = 4
                        elif tracker ==4:
                            tracker =1 
                        else:
                            print "Wtf this shouldn't happen."
            else:
                playlist = False
                pass

            return playlist
        
        except urllib2.HTTPError, e:
            print "Cannot retreieve URL: HTTP Error Code", e.code
        except urllib2.URLError, e:
            print "Cannot retrieve URL: " + e.reason[1]


    def lyrics(self, artist, song):
        'Enter artist and song to find lyrics on one of two online databases'
        song = song.replace(',','')
        try:
            begin = artist[0]+artist[1]+artist[2]
            if begin.lower() == 'the':
                artist = artist[4:]

        
            address = 'http://www.azlyrics.com/lyrics/' + \
                      artist.replace(' ', '').lower() + '/' + \
                      song.replace(' ', '').lower() + '.html'
            web_handle = urllib2.urlopen(address)
            web_text = web_handle.read()
            lyrics = sre.findall('(?s)<!-- start of lyrics -->(.*?)<!', web_text, sre.MULTILINE)
            lyrics = lyrics[0]
            lyrics.replace('\n', '')
            lyrics.replace('\r\n', '')
            return lyrics
        except urllib2.HTTPError, urllib2.URLError: # if not found, try different website
            try:
                begin = artist[0]+artist[1]+artist[2]
                if begin.lower() == 'the':
                    artist = artist[4:]
                    
                address = 'http://indierocklyrics.com/' + \
                          artist.replace(' ', '-').lower() + '/' + \
                          song.replace(' ', '-').lower() + '-lyrics'
                web_handle = urllib2.urlopen(address)
                web_text = web_handle.read()
                lyrics = sre.findall('(?s)<p>\&nbsp;<br\ />(.*?)<a\ href\=\"http://www'\
                                     , web_text, sre.MULTILINE)
                lyrics = lyrics[0]
                lyrics.replace('\n', '')
                lyrics.replace('\r\n', '')
                return lyrics
            except urllib2.HTTPError, e:
                print "Cannot retreieve URL: HTTP Error Code", e.code
            except urllib2.URLError, e:
                print "Cannot retrieve URL: " + e.reason[1] 

            
    
    def update(self):
        'Method that updates database every time someone tries to look up info in case new shows happened'
        blank = 15 # guess that there will not be a strech of x blank shows in a row.
                   # (Even if a show didn't happen or didn't yet occur, the webpage still exists)
        
        start = int(self.last_page)  # constants for loops
        end = start + blank
        no_playlist_count = 0
        
        while no_playlist_count < blank:  # parse pages in batches, in case we get to end of playlists with data
            no_playlist_count = 0   

            for page in range(start, end):
                if self.load('http://www.wqhs.org/playlist.php?id='+ str(page)) == True:
##                    if page % 100 == 0: # print out every 100th page for sanity checks
##                        print page
                    self.last_page = '%d' % page
                    save = open('last_page.txt', 'w')
                    save.write(self.last_page)
                    save.close
                else: # if playlist wasn't made for that show
##                    print "No playlist: %d" % page 
                    no_playlist_count += 1

            start = start + blank
            end = start + blank

            save = open('WQHSdata.txt', 'w')
            save.write(str(self.data))
            save.close()

            

    def cover_art(self, query):
        'Enter album name to get link to cover art'
        
        query = query.replace(',','')
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
