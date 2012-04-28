'Provides functions to add songs from WQHS.org to music database (stored as nested dictionary) \
and to lookup information about most frequently played things on the radio'

import time 
from datetime import date 

class WQHS(object):

    def __init__(self):
        'Stores database'
        
        self.data = {}
        self.today = date.today()
        self.today = self.today.isocalendar()

        #sample data
        self.data = {'the beatles': {'the white album': {'revolution': [(2012, 15, 7), (2012, 1, 7)],\
                                                         'song 1'    : [(2011, 15, 4)]},
                                     'let it be'      : {'let it be' : [(2011, 15, 1), (2011, 2, 3)], \
                                                         'song 1'    : [(2012, 15, 3), (2009, 2, 2)]}},
                     'lcd soundsystem':{'sound of silver':{'all my friends': [(2008, 17, 3), (2008, 17, 3), (2011, 17, 3)]}}}

                                           
    def lookup_artist(self, artist):
        'Enter name of artist to see how many songs by them were played'
        
        count = 0
        artist = artist.lower()
       
        for albums in self.data[artist].values():
            for songs in albums.values():
                count += len(songs)

        print '%d Songs Played By %s' % (count, artist)

        
    def timespan_select(self, timespan):
        'Enter timespan to see top played artist, album, and song in that timespan \
        possible arugments for timespan = last year, last month, last week, all time, or custom'

        'if custom is chosen, format is a tuple (start date, end date)\
        where the start date is the later date, and the end date is the more recent date '

        end = self.today
        
        if timespan == 'last year':
            start = (self.today[0]-1, self.today[1], self.today[2])
        elif timespan == 'last month':
            start = (self.today[0], self.today[1]-4, self.today[2])
        elif timespan == 'last week':
            start = (self.today[0], self.today[1]-1, self.today[2])
        elif timespan == 'all time':
            start = (2006, 1, 1)                                                  
        elif isinstance(timespan, tuple): # if custom date range is passed in as tuple
            start = timespan[0]
            end = timespan[1]
        
        return self.lookup_freq(start, end, timespan) # call the lookup_freq function with specified timespan


    def lookup_freq(self, start, end, timespan):

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
                        if date >= start and date <= end: # check ranges of dates (most inner loop)
                            song_count += 1
                            album_count += 1
                            
                    if song_count > top_song[0]: # after iterating through dates check if song beats the top spot
                        top_song   = [song_count, song, artist, album]

                artist_count += album_count                
                if album_count > top_album[0]: # after iterating songs check if album beats the top spot
                    top_album = [album_count, album, artist]


            if artist_count > top_artist[0]: # after iterating through albums check if artist beats the top spot
                top_artist = [artist_count, artist]

        
        artist_result = 'Most played artist of %s is: %s' % (timespan, top_artist[1])
        album_result = 'Most played album  of %s is: %s by %s'  % (timespan, top_album[1], top_album[2])
        song_result = 'Most played song   of %s is: %s, by %s off of their album, %s' % (timespan, top_song[1], top_song[2], top_song[3])

        print artist_result
        print album_result
        print song_result
        print ''

        return artist_result, album_result, song_result
        
    
    def add_song(self, artist, album, song):
        'Enter name of artist, album, and song to add it to the database'

        artist = artist.lower()
        album = album.lower()
        song = song.lower()

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
    
    test.lookup_artist('the beatles')
    test.add_song('lcd soundsystem', 'sound of silver', 'north american scum')
    
    test.timespan_select('all time')
    test.timespan_select('last year')

    custom_range = ((2008, 17, 3), (2008, 17, 4))
    test.timespan_select(custom_range)

    

    
