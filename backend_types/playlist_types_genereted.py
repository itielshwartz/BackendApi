import datetime

__author__ = 'ishwartz'


# This a basic represent of a single voting - playlist
# it include the playlist id, current votes , songs and last time it was updated.
class gen_playlist:
    id = ""
    votes = []
    songs = []
    time_change = datetime.datetime.now().time()

    def __init__(self, id, songs):
        self.id = id
        self.songs = songs
        self.votes = [0 for i in range(len(songs))]
        self.time_change = datetime.datetime.now().time()

    def add_vote(self, i):
        self.votes[i] += 1

    def sub_vote(self, i):
        self.votes[i] -= 1

    def get_max_song(self):
        return self.songs[self.votes.index(max(self.votes))]

