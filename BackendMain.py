"""Hello World API implemented using Google Cloud Endpoints.
Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import random

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from PlayListStub import playlistIdToName




# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
from backend_types.playlist_types_db import PlaceDB
from backend_types.playlist_types_api import Place, Song, androidPlaylist
from backend_types.playlist_types_genereted import current_playlists
from backend_types.youtube_data_wrapper import get_youtube_playlist

WEB_CLIENT_ID = '572283433642-27216moiovs3calv9clvqtimsqmldi2e.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

# package = 'Hello'

DEFAULT_PLAYLIST_SIZE = 7
PLAYLIST_ORIGINAL_SIZE = 11


def generateAndroidPlaylist():
    genList = [0 for _ in xrange(DEFAULT_PLAYLIST_SIZE)]
    i = 0
    while i < DEFAULT_PLAYLIST_SIZE:
        r = random.randint(0, PLAYLIST_ORIGINAL_SIZE - 1)
        if r not in genList:
            genList[i] = r
            i += 1
    songslist = [] * DEFAULT_PLAYLIST_SIZE
    for i in xrange(DEFAULT_PLAYLIST_SIZE):
        songslist.append(Song(pos=genList[i], name=playlistIdToName[genList[i]]))
    genPlaylist = androidPlaylist(songs=songslist)
    return genPlaylist


def convert_playlist(playlist):
    pass


@endpoints.api(name='voTunes', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, 'endpoints.API_EXPLORER_CLIENT_ID'],
               audiences=[ANDROID_AUDIENCE])
class voTunesApi(remote.Service):
    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1),
    )

    # summery:
    # Returns the next song to be played(max votes) in accordance with received key.
    @endpoints.method(ID_RESOURCE, Song,
                      path='getNextSongId/{id}', http_method='GET',
                      name='getNextSongId')
    def voTunes_getNextSong(self, request):
        currentPlace = current_playlists.get_max_vote(id)
        #to do add genreted
        return Song(pos=currentPlace)

    ID_RESOURCE_S = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    #summery:
    #Returns the current playlist in accordance with received key.
    @endpoints.method(ID_RESOURCE_S, androidPlaylist,
                      path='getListOfSongs/{id}', http_method='GET',
                      name='getListOfSongs')
    def voTunes_getListOfSongs(self, request):
        playlist = current_playlists.get_current_songs(id)
        msg_playlist = convert_playlist(playlist)
        return msg_playlist

    ID_RESOURCE_P = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1),
        play_list_id=messages.StringField(2))

    #summery:
    #Received generated key and creates an entity in the DB as a new place
    @endpoints.method(ID_RESOURCE_P, Song,
                      path='addPlaylistandUserKey/', http_method='GET',
                      name='addPlaylistandUserKey')
    def voTunes_getPlaylistandUserKey(self, request):
        my_playlist = get_youtube_playlist(request.play_list_id)
        ps = PlaceDB(play_list=my_playlist, id=request.id)
        ps.put()
        return Song(name=my_playlist)


ID_RESOURCE_P_Test = endpoints.ResourceContainer(
    message_types.VoidMessage,
    id=messages.StringField(1),
    up=messages.IntegerField(2),
    down=messages.IntegerField(3))

# summery:
# Received generated key, and 2 chars representing 2 songs in playlist.
#First char is for increment. Second char is for decrement(in case of changing the song choice).
#For both chars - 'I' represents ignore choice.
@endpoints.method(ID_RESOURCE_P_Test, Place,
                  path='voteForSong/{id}', http_method='GET',
                  name='voteForSong')
def voTunes_voteForSong(self,
                        request):  #id format: <id-6 numbers><song-digit-for-vote-up><song-digit-for-vote-down> (digit '9' means do not vote down any song)
    id = request.id
    up = request.up
    down = request.down
    votes = current_playlists.vote(id, up, down)
    return Place(currentVotes=votes)


APPLICATION = endpoints.api_server([voTunesApi])