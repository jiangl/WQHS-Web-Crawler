README 
CIS 192 Final project

Alejandra Murphy Judy (alejm)
Aldrin Abastillas (aldrin)
Lisa Jiang (jiangl)

WQHSCrawler.py contains the code that searches the WQHS website to find the playlist information from each show, 
as well as the code the places that information into a dictionary, which is stored for later use in either WQHSdata.txt
 (if you are running the algorithm fresh, and this document doesn't exist, it will be created), or into last_page.txt, 
which is where updates are placed. This file can't be run on its own.

WidgetWQHS.py contains the GUI (a simple, separate window) through which a user can access the information found 
and stored by WQHSCrawler.py. This can be run as a module in IDLE. 

The folder coverart contains the necessary files to run the coverart module used in WQHSCrawler to find urls for the coverart
of the results of a search. It shouldn't be run on its own.



*In the end, we could not put the widget onto the WQHS website; there wasnt enough server space available to handle the
stored dictionary file. 

*The folder js-widget(extra) contains the original javascript widget (made in pyjamas) that we ended up scrapping. This isn't acutally
being used, but you can look at it if you like; the functional GUI is written just in python, using Tkinter. The widget can be seen
by going to js-widget(extra) -> output -> Widget.html. You may need to use explorer to actually see it. Again, however, this
is not a part of the project; we're not expecting extra credit or any points whatsoever for this.


