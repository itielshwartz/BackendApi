from google.appengine.ext import ndb

__author__ = 'ishwartz'




class SongDB(ndb.Model):
    length = ndb.StringProperty()
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    pos = ndb.IntegerProperty()



class PlayListDB(ndb.Model):
    id = ndb.StringProperty()
    items = ndb.StructuredProperty(SongDB, repeated=True)




class PlaceDB(ndb.Model):
    play_list = ndb.StructuredProperty(PlayListDB, repeated=False)