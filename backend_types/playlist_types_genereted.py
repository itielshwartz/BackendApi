import datetime

__author__ = 'ishwartz'

class gen_playlist:
    id = ""
    votes = []
    time_change = datetime.datetime.now().time()

    def __init__(self,id,size):
        self.id = id
        self.votes = [0 for 0 in range(size)]
        self.time_change = datetime.datetime.now().time()

    def addVote(self,i):
        self.votes[i] = self.votes[i] + 1

    def subVote(self,i):
        self.votes[i] = self.votes[i] - 1


class all_gen_playlist:
    dic = dict()

    def add_playlist(self,key,size):
        self.dic[key] = gen_playlist(id,size)