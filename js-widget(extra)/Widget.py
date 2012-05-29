import pyjd # this is dummy in pyjs.
import pygwt

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea

class SongFrequency:

    def __init__(self):
        self.artist =''
        self.start_date = ''
        self.end_date = ''
        self.period_search =''
        self.search_option = 1
        #declare the general interface widgets
        self.panel = DockPanel(StyleName = 'background')
        self.ret_area = TextArea()
        self.ret_area.setWidth("350px")
        self.ret_area.setHeight("90px")
        self.options = ListBox()

        self.search_button = Button("Search", getattr(self, "get_result"), StyleName = 'button')

        #set up the date search panel; it has different text boxes for
        #to and from search dates
        self.date_search_panel = VerticalPanel()
        self.date_search_start = TextBox()
        self.date_search_start.addInputListener(self)
        self.date_search_end = TextBox()
        self.date_search_end.addInputListener(self)
        
        self.date_search_panel.add(HTML("Enter as month/day/year", True, StyleName = 'text'))
        self.date_search_panel.add(HTML("From:", True, StyleName = 'text'))
        self.date_search_panel.add(self.date_search_start)
        self.date_search_panel.add(HTML("To:", True, StyleName = 'text'))
        self.date_search_panel.add(self.date_search_end)
        #set up the artist search panel
        self.artist_search = TextBox()
        self.artist_search.addInputListener(self)
        self.artist_search_panel = VerticalPanel()
        self.artist_search_panel.add(HTML("Enter artist's name:",True,
                                          StyleName = 'text'))
        self.artist_search_panel.add(self.artist_search)

        #Put together the list timespan search options
        self.period_search_panel = VerticalPanel()
        self.period_search_panel.add(HTML("Select a seach period:",True,
                                          StyleName = 'text'))
        self.period_search = ListBox()
        self.period_search.setVisibleItemCount(1)
        self.period_search.addItem("last week")
        self.period_search.addItem("last month")
        self.period_search.addItem("last year")
        self.period_search.addItem("all time")
        self.period_search_panel.add(self.period_search)
        #add the listeners to the appropriate widgets
        self.options.addChangeListener(self)
        self.period_search.addChangeListener(self)
        self.ret_area_scroll = ScrollPanel()
        self.search_panel = HorizontalPanel()
        self.options_panel = VerticalPanel()

    # A change listener for the boxes
    def onChange(self, sender):
        #switch the list box options
        if sender == self.options:
            self.search_panel.remove(self.period_search_panel)
            self.search_panel.remove(self.date_search_panel)
            self.search_panel.remove(self.artist_search_panel)

            index = self.options.getSelectedIndex()

            if index == 0:
                self.search_panel.add(self.artist_search_panel)
                self.search_option = 1
            elif index == 1:
                self.search_panel.add(self.date_search_panel)
                self.search_option = 2
            elif index == 2:
                self.search_panel.add(self.period_search_panel)
                self.search_option = 3

        elif sender == self.period_search:
            index = self.period_search.getSelectedIndex()
            if index == 0:
                self.period_search = "last week"
            elif index == 1:
                self.period_search = "last month"
            elif index == 2:
                self.period_search = "last year"
            elif index == 3:
                self.period_search = "all time"

    #A listener for the text boxes            
    def onInput(self, sender):
        if sender == self.artist_search:
            self.artist = sender.getText()
        elif sender == self.date_search_end:
            self.end_date = sender.getText()
        elif sender == self.date_search_start:
            self.start_date = sender.getText()

    #A listener for the buttons that, when the button is clicked, looks up the results and outputs them
    def get_result(self):
        return_str = " "
        if self.search_option == 1:
            return_str = self.artist
        elif self.search_option == 2:
            return_str = self.start_date
        elif self.search_option ==3:
            return_str = self.period_search
        else:
            return_str = "Find the most played artist, album, or song for a time period, or the number of songs played by a certain artist"
        self.ret_area.setText(return_str)

   
    def onModuleLoad(self):
        #Put together the list of options
        self.options.addItem("Artist")
        self.options.addItem("Date")
        self.options.addItem("Time Span")
        self.options.setVisibleItemCount(3)

        #put the text area together
        self.ret_area_scroll.add(self.ret_area)
        self.ret_area.setText("Find the most played artist, album, or song for a time period, or the number of songs played by a certain artist")
        #put the search items together
        self.search_panel.add(self.artist_search_panel)
        #Put together the options panel
        self.options_panel.add(HTML("Search By:", True, StyleName = 'text'))
        self.options_panel.add(self.options)
        #Add everything to the main panel
        self.panel.add(HTML("WQHS Song Search",True, StyleName = 'header'),
                       DockPanel.NORTH)

        self.panel.add(self.options_panel, DockPanel.WEST)
        
        self.panel.add(self.ret_area_scroll, DockPanel.SOUTH)
        self.panel.setCellHeight(self.ret_area_scroll, "100px")
        self.panel.setCellWidth(self.ret_area_scroll, "300px")

        self.panel.add(self.search_button, DockPanel.EAST)
        
        self.panel.add(self.search_panel, DockPanel.CENTER)
    
        #Associate panel with the HTML host page
        RootPanel().add(self.panel)
                

if __name__ == '__main__':
    widg = SongFrequency()

    widg.onModuleLoad()
