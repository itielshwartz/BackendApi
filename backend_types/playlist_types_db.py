from google.appengine.ext import ndb

__author__ = 'ishwartz'


class SongDB(ndb.Model):
    id = ndb.StringProperty()
    length = ndb.StringProperty()
    name = ndb.StringProperty()
    pos = ndb.IntegerProperty()


class PlayListDB(ndb.Model):
    items = ndb.StructuredProperty(SongDB, repeated=True)


class PlaceDB(ndb.Model):
    loc = ndb.StringProperty()
    play_list_history = ndb.StringProperty(repeated=True)
    current_play_list = ndb.StringProperty()
    enable = ndb.BooleanProperty(default=True)
    size_of_play_list = ndb.IntegerProperty(default=7)

    def get_current_playlist(self):
        return PlayListDB.get_by_id(self.current_play_list)