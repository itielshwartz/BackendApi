from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from backend_types.playlist_types_db import PlayListDB

__author__ = 'ishwartz'


class webPlayList(messages.Message):
    data = messages.StringField(2) #the position of the song in the original YouTube playlist


class Song(messages.Message):
    pos = messages.IntegerField(1) #the position of the song in the original YouTube playlist
    name = messages.StringField(2)
    youtubeUrl = messages.StringField(3)

class androidPlaylist(messages.Message):
    id = messages.IntegerField(1) # the original playlist id of Youtube
    songs = messages.MessageField(Song, 2, repeated=True) # these are the songs that are displayed in the android
    selectedSongsHistory = messages.IntegerField(3, repeated=True) #list of songs that has been chosen

class Place(messages.Message):
    name = messages.StringField(1)
    generatedKey = messages.IntegerField(2)
    playingPlaylist = messages.MessageField(androidPlaylist, 3) # the playlist that is being displayed in the android
    currentVotes = messages.IntegerField(4, repeated=True)

