import socket; socket.setdefaulttimeout(10)

class CoverSourceBase(object):

    def __init__(self):
        self.max_results = 10
        self.active = True

    def search(self, query):
        pass
