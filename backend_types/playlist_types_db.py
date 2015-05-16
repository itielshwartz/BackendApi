from google.appengine.ext import ndb

__author__ = 'ishwartz'




class SongDB(ndb.Model):
    length = ndb.StringProperty()
    id = ndb.StringProperty()
    name = ndb.StringProperty()

    def __str__(self):
        return "id :" + str(self.id) + " name: " + str(self.name) + " length : " + str(self.length)


class PlayListDB(ndb.Model):
    id = ndb.StringProperty()
    items = ndb.StructuredProperty(SongDB, repeated=True)

    def __str__(self):
        return "id :" + str(self.id) + " items: " +  '\n'.join(map(str, self.items))



class PlaceDB(ndb.Model):
    play_list = ndb.StructuredProperty(PlayListDB, repeated=False)