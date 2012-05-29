#!/usr/bin/python

import Tkinter
from WQHSCrawler import *

class WQHSWidget(Tkinter.Tk):
    def __init__(self, parent):
        #start the GUI
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.crawler = WQHS()
        self.initialize()


    def initialize(self):
        #Set the layout, background color
        self.grid()
        self.config(background = '#FFFFCC')
        headerfont = ('Helvetica', 14)
        menufont = ('Helvetica', 12)

        intro = Tkinter.Label(self, text ="Search for most frequently played songs by artist, date, or time period.",
                              fg = "#6655BB", bg = '#FFFFCC', font =headerfont, bd = 10)
        #Make the options buttons
        self.selection = Tkinter.IntVar()
        self.artist_box= Tkinter.Radiobutton(self, text="Search by artist",
                                             variable = self.selection, value = 1, command= self.switch,
                                             fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD', font = menufont)
        self.date_box= Tkinter.Radiobutton(self, text="Search by date",
                                            variable = self.selection, value = 2, command= self.switch,
                                           fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD', font = menufont)
        self.period_box= Tkinter.Radiobutton(self, text="Search by time period",
                                              variable = self.selection, value = 3, command= self.switch,
                                             fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD', font= menufont)

        #Place the options
        intro.grid(row = 0, column = 0)
        self.artist_box.grid(row = 1, column=0)
        self.date_box.grid(row = 2, column=0)
        self.period_box.grid(row = 3, column=0)
        #make the widgets for later use
        self.date_to = Tkinter.Entry(self)
        self.date_from = Tkinter.Entry(self)
        self.artist_entry = Tkinter.Entry(self)
        self.label = Tkinter.Label(self, text ="Enter artist's name:", fg = "#6655BB", bg = '#FFFFCC')
        self.to = Tkinter.Label(self, text ="End date(m/d/y):", fg = "#6655BB", bg = '#FFFFCC')
        self.from_d = Tkinter.Label(self, text ="Start date(m/d/y):", fg = "#6655BB", bg = '#FFFFCC')

        self.period_select = Tkinter.IntVar()
        self.lstwk= Tkinter.Radiobutton(self, text="last week",
                                             variable = self.period_select, value = 1,
                                        fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD')
        self.lstmnth= Tkinter.Radiobutton(self, text="last month",
                                            variable = self.period_select, value = 2,
                                          fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD')
        self.lstyear= Tkinter.Radiobutton(self, text="last year",
                                              variable = self.period_select, value = 3,
                                          fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD')
        self.allt= Tkinter.Radiobutton(self, text="all time",
                                              variable = self.period_select, value = 4,
                                       fg = "#6655BB", bg = '#FFFFCC', activebackground = '#66DDDD')
        #Make the result panel for later use
        #self.ret_frame = Tkinter.Frame(self)
        #self.ret_frame.pack()
        self.scrollbar = Tkinter.Scrollbar(self, orient='vertical', bg ="#6655BB")
        self.result_list = Tkinter.Listbox(self, width = 80, yscrollcommand= self.scrollbar.set)
        self.scrollbar.config(command=self.result_list.yview)
        #self.scrollbar.pack(side='right', fill = 'y')
        #self.result_list.pack(side = 'left', fill = 'both', expand= 1)


        #Make and place the search button
        self.search_button = Tkinter.Button (self, text = "Search", command = self.search_click)
        self.search_button.grid(row = 4, column=0)

#Switch the options
    def switch(self):
        #remove what's there
        self.search_button.grid_forget()
        self.date_to.grid_forget()
        self.date_from.grid_forget()
        self.artist_entry.grid_forget()
        self.label.grid_forget()
        self.to.grid_forget()
        self.from_d.grid_forget()

        self.lstwk.grid_forget()
        self.lstmnth.grid_forget()
        self.lstyear.grid_forget()
        self.allt.grid_forget()
        self.result_list.grid_forget()
        self.scrollbar.grid_forget()
        #draw the appropriate things
        if self.selection.get() ==1 :
            self.label.grid(row =5, sticky = 'W')
            self.artist_entry.grid(row = 5,column=0)
            self.search_button.grid(row = 6, column=0)
        elif self.selection.get() ==2 :
            self.to.grid(row = 5,sticky = 'W')
            self.from_d.grid(row = 6,sticky = 'W')
            self.date_to.grid(row =5, column = 0)
            self.date_from.grid(row =6, column = 0)
            self.search_button.grid(row = 7, column = 0)
        elif self.selection.get()==3:
            self.lstwk.grid(row = 5,sticky = 'EW')
            self.lstmnth.grid(row = 6,sticky = 'EW')
            self.lstyear.grid(row = 7,sticky = 'EW')
            self.allt.grid(row = 8,sticky = 'EW')
            self.search_button.grid(row = 9, column = 0)

#CLick button response; looks up the appropriate values, and returns them in a listbox
    def search_click(self):
        #Clear the view below the options area
        self.date_to.grid_forget()
        self.date_from.grid_forget()
        self.artist_entry.grid_forget()
        self.label.grid_forget()
        self.to.grid_forget()
        self.from_d.grid_forget()

        self.lstwk.grid_forget()
        self.lstmnth.grid_forget()
        self.lstyear.grid_forget()
        self.allt.grid_forget()
        #Clear the listbox and redraw it
        result = ""
        self.result_list.delete(0, 'end')
        self.result_list.grid(row= 5, sticky = 'W')
        self.scrollbar.grid(row=5, sticky= 'NE')
        #Artist search
        if self.selection.get() == 1:
            artist_search = self.artist_entry.get()
            result = self.crawler.lookup_artist(artist_search)
            self.result_list.insert(0, result)
        #Date search
        elif self.selection.get() ==2:
            to_d = self.date_to.get()
            from_d = self.date_from.get()
            tosend = self.date_change(to_d)
            fromsend = self.date_change(from_d)
            if tosend and fromsend:
                try:
                    result_temp = self.crawler.timespan_select((fromsend, tosend))
                except IndexError:
                    result_temp = "Woops! We're having technical difficulties.%n Please try some different dates"
                self.process_return(result_temp)
            else:
                result = "That is not a valid date entry."
                self.result_list.insert(0,result)
        #Period Search
        elif self.selection.get()==3:
            result_temp = 0,0
            if self.period_select.get() ==1:
                result_temp = self.crawler.timespan_select('last week')
            elif self.period_select.get() ==2:
                result_temp = self.crawler.timespan_select('last month')
            elif self.period_select.get() ==3:
                result_temp = self.crawler.timespan_select('last year')
            elif self.period_select.get() ==1:
                result_temp = self.crawler.timespan_select('all time')
            self.process_return(result_temp)
        else:
            self.result_list.insert(0, "Thats not a valid option!")

#A helper method to take care of processing return tuples
    def process_return(self, return_tupl):
        index = 0
        for res in return_tupl:
            if index == 3:
                self.result_list.insert(index, "Go to this URL for the top album's artwork:")
                index +=1
            elif index == 5:
                self.result_list.insert(index, "Go to this URL for the top song's artwork:")
                index +=1
            elif index == 7:
                self.result_list.insert(index, "Top song's lyrics:")
                self.lyrics_process(res,index+1)
                break
            self.result_list.insert(index, res)    
            index +=1
            
#Process the lyrics
    def lyrics_process(self, lyrics, ind):
        line_list = lyrics.split('<br>')
        for line in line_list:
            self.result_list.insert(ind, line)
            ind+=1

#Change the input date       
    def date_change(self, date):
        in_list = date.split('/')
        if len(in_list)== 3:
            if in_list[0].isdigit() and in_list[1].isdigit() and in_list[2].isdigit():
                return int(in_list[2]), int(in_list[1]), int(in_list[0])

        
if __name__ == "__main__":
    app = WQHSWidget(None)
    app.title('Song Search widget')
    app.mainloop()
