''

import time 
from datetime import date 

class WQHS(object):

    def __init__(self):
        'Stores database'
        
        self.data = {}
        self.today = date.today()
        self.today = self.today.isocalendar()
        self.alltime_song = ''
        self.alltime_artist = ''

        #sample data
        self.data = {'the beatles': {'the white album': {'revolution': [(2012, 15, 7), (2012, 1, 7)],\
                                                         'song 1'    : [(2011, 15, 4)]},
                                     'let it be'      : {'let it be' : [(2011, 15, 1), (2011, 2, 3)], \
                                                         'song 1'    : [(2012, 15, 3), (2009, 2, 2)]}},
                     'lcd soundsystem':{'sound of silver':{'all my friends': [(2012, 17, 3), (2012, 17, 3), (2011, 17, 3)]}}}

                                           
    def lookup_artist(self, artist):
        'Enter name of artist to see how many songs by them were played'
        
        count = 0

##        artist = raw_input("Enter artist: ")
       
        for albums in self.data[artist.lower()].values():
            for songs in albums.values():
                count += len(songs)

        print '%d Songs Played By %s' % (count, artist)

        
    def lookup_freq(self, time):
        'Enter timespan to see top played artist, album, and song in that timespan'

        print 'Enter timespan to see top played artist, album, and song'
        print 'Last year, last month, last week, all time, or custom'

        print ''
        print 'Today is:'
        print self.today 

##        time = raw_input("Enter timespan: ")
        time = time.lower()

        top_artist = [0]
        top_album  = [0]
        top_song   = [0]

        if time == 'last year':
            print time
        elif time == 'last month':
            print time
        elif time == 'last week':
            print time
        elif time == 'all time':
            for artist in self.data.keys():
                temp_count = 0 # temp count for number songs in each album for artist              
                for album in self.data[artist].keys():
                    album_count = len(self.data[artist][album].values())
                    temp_count += album_count
                    if album_count > top_album[0]: # find top album
                        top_album = [album_count, album, artist]
                    
                    for song in self.data[artist][album].keys():
                        song_count = len(self.data[artist][album][song]) 
                        if song_count > top_song[0]: # find top song
                            top_song   = [song_count, song, artist, album]

                if temp_count > top_artist[0]: # after iterating through albums, compare and save top artist
                    top_artist = [temp_count, artist]
                                        
        elif time == 'custom':
            print time

        print ''
        print 'Most played artist of %s is: %s' % (time, top_artist[1])
        print 'Most played album  of %s is: %s by %s'  % (time, top_album[1], top_album[2])
        print 'Most played song   of %s is: %s, by %s off of their album, %s' % (time, top_song[1], top_song[2], top_song[3])
        

        

    def add_song(self, artist, album, song):
        'Enter name of artist, album, and song to add it to the database'

##        artist = raw_input("Enter artist: ")
        artist = artist.lower()
        
##        album  = raw_input("Enter album: ")
        album  = album.lower()
        
##        song   = raw_input("Enter song: ")
        song   = song.lower()

        if artist not in self.data:
            self.data[artist] = {}
            self.data[artist][album] = {}
            self.data[artist][album][song] = self.today
            
        elif album not in self.data[artist].keys():
            self.data[artist][album] = {}
            self.data[artist][album][song] = self.today
            
        elif song not in self.data[artist][album].keys():
            self.data[artist][album][song] = self.today           
        else:
            self.data[artist][album][song].append(self.today)
            
                                   
if __name__ == "__main__":
    
    test = WQHS()
    data = test.data
##    test.lookup_artist()
##    test.add_song()
    test.lookup_freq()

##    print ""
##    print "data:"
##    print data
    

    
