import datetime

__author__ = 'ishwartz'


class gen_playlist:
    id = ""
    votes = []
    songs = []
    time_change = datetime.datetime.now().time()

    def __init__(self, id, size, original):
        self.id = id
        self.votes = [0 for 0 in range(size)]
        self.original_place = original
        self.time_change = datetime.datetime.now().time()

    def add_vote(self, i):
        self.votes[i] += 1

    def sub_vote(self, i):
        self.votes[i] -= 1

    def get_max_song(self, i):
        self.original_place[self.votes.index(max(self.votes))]


class all_gen_playlist:
    def __init__(self):
        pass

    dic = dict()

    def add_playlist(self, key, size, original):
        self.dic[key] = gen_playlist(id, size, original)

    def add_vote(self, key, i):
        self.dic.get(key).add_vote(i)
        return self.dic.get(key).votes

    def sub_vote(self, key, i):
        self.dic.get(key).sub_vote(i)
        return self.dic.get(key).votes

    def get_max_vote(self, key, i):
        return self.dic.get(key).get_max_song()

    def vote(self, key, up, down):
        self.dic.get(key).add_vote(up)
        if (down > -1):
            self.dic.get(key).sub_vote(down)
        return self.dic.get(key).votes


    def get_current_songs(self, key):
        return self.dic.get(key).songs


current_playlists = all_gen_playlist()