''

import time 
from datetime import date 

class WQHS(object):

    def __init__(self):
        'Stores database'
        
        self.data = {}
        self.today = date.today()
        self.today = self.today.isocalendar()
        self.top_song = ''
        self.top_artist = ''

        #sample data
        self.data = {'the beatles': {'the white album': {'revolution': [(2012, 15, 7), (2012, 1, 7)],\
                                                         'song 1'    : [(2011, 15, 4), (2012, 2, 4)]},
                                     'let it be'      : {'let it be' : [(2011, 15, 1), (2011, 2, 3)], \
                                                         'song 1'    : [(2012, 15, 3), (2009, 2, 2)]}}}

                                           
    def lookup_artist(self):
        'Enter name of artist to see how many songs by them were played'
        
        count = 0

        artist = raw_input("Enter artist: ")
       
        for albums in self.data[artist.lower()].values():
            for songs in albums.values():
                count += len(songs)

        print '%d Songs Played By %s' % (count, artist)

        

    def lookup_freq(self):
        'Enter timespan to see top played artist, album, and song in that timespan'

        print 'Enter timespan to see top played artist, album, and song'
        print 'Last year, last month, last week, or all time'

        print ''
        print self.today 

        time = raw_input("Enter timespan: ")
        time = time.lower()

        if time == 'last year':
            print time
        elif time == 'last month':
            print time
        elif time == 'last week':
            print time
        elif time = 'all time':
            print time 

        

    def add_song(self):
        'Enter name of artist, album, and song to add it to the database'

        artist = raw_input("Enter artist: ")
        artist = artist.lower()
        
        album  = raw_input("Enter album: ")
        album  = album.lower()
        
        song   = raw_input("Enter song: ")
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
##    test.lookup_artist()
##    test.add_song()
    test.lookup_freq()

    print ""
    print "data:"
    print test.data
    

    
