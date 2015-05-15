__author__ = 'ishwartz'


class PlayList:
    id = "id"
    items = []

    def __init__(self, playlist_id, items):
        self.id = playlist_id
        self.items = items

    def __str__(self):
        return "id :" + str(self.id) + " items: " +  '\n'.join(map(str, self.items))


class Song:
    length = ""
    id = ""
    name = ""

    def __init__(self, id, name, length):
        self.id = id
        self.name = name
        self.length = length

    def __str__(self):
        return "id :" + str(self.id) + " name: " + str(self.name) + " length : " + str(self.length)