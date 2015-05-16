
import random

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from PlayListStub import playlistIdToName

from google.appengine.api import memcache



# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
from backend_types.playlist_types_db import PlaceDB, PlayListDB
from backend_types.playlist_types_api import Place, Song, androidPlaylist
from backend_types.playlist_types_genereted import current_playlists, gen_playlist
from backend_types.youtube_data_wrapper import get_youtube_playlist

WEB_CLIENT_ID = '572283433642-27216moiovs3calv9clvqtimsqmldi2e.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

# package = 'Hello'

DEFAULT_PLAYLIST_SIZE = 7
PLAYLIST_ORIGINAL_SIZE = 11

def generatePlaylist(id):
    currentPlace = PlaceDB.get_by_id(id)
    youtubePlaylist = currentPlace.play_list
    songsList = []
    max_size = min(DEFAULT_PLAYLIST_SIZE,len(youtubePlaylist.items))
    songsNumbers = random.sample(range(len(youtubePlaylist.items)), max_size)
    for song in songsNumbers:
        songsList.append(youtubePlaylist.items[song])
    return songsList

def convert_playlist(playlist):
    csongs = androidPlaylist()
    for song in playlist:
        csongs.songs.append(Song(pos = song.pos, name = song.name))
    return csongs


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
        currentPlace = memcache.get(request.id).get_max_song()
        temp_playlist = generatePlaylist(request.id)
        q = gen_playlist(request.id, temp_playlist)
        memcache.replace(request.id,q)
        # to do add genreted
        return Song(pos=currentPlace.pos)

    ID_RESOURCE_S = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    # summery:
    # Returns the current playlist in accordance with received key.
    @endpoints.method(ID_RESOURCE_S, androidPlaylist,
                      path='getListOfSongs/{id}', http_method='GET',
                      name='getListOfSongs')
    def voTunes_getListOfSongs(self, request):
        playlist = memcache.get(request.id).songs
        msg_playlist = convert_playlist(playlist)
        return msg_playlist

    ID_RESOURCE_P = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1),
        play_list_id=messages.StringField(2))

    # summery:
    # Received generated key and creates an entity in the DB as a new place
    @endpoints.method(ID_RESOURCE_P, androidPlaylist,
                      path='addPlaylistandUserKey/', http_method='GET',
                      name='addPlaylistandUserKey')
    def voTunes_getPlaylistandUserKey(self, request):
        my_playlist = get_youtube_playlist(request.play_list_id)
        ps = PlaceDB(play_list=my_playlist, id=request.id)
        ps.put()
        temp_playlist = generatePlaylist(request.id)
        q = gen_playlist(request.id, temp_playlist)
        memcache.add(request.id,q)
        android_playlist  = convert_playlist(temp_playlist)
        return android_playlist

    ID_RESOURCE_P_Test = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1),
        up=messages.IntegerField(2),
        down=messages.IntegerField(3))

    # summery:
    # Received generated key, and 2 chars representing 2 songs in playlist.
    # First char is for increment. Second char is for decrement(in case of changing the song choice).
    # For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_P_Test, Place,
                      path='voteForSong/', http_method='GET',
                      name='voteForSong')
    def voTunes_voteForSong(self, request):
        id = request.id
        up = request.up
        down = request.down
        playlist = memcache.get(request.id)
        playlist.votes[up] +=1
        if(down):
            playlist.votes[down] -=1
        memcache.replace(id,playlist)
        return Place(currentVotes=playlist.votes)

  # summery:
    # Received generated key, and 2 chars representing 2 songs in playlist.
    # First char is for increment. Second char is for decrement(in case of changing the song choice).
    # For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_P_Test, Place,
                      path='getSongsVote/', http_method='GET',
                      name='getSongsVote')
    def voTunes_getsongs_vote(self, request):
        votes = memcache.get(request.id).votes
        return Place(currentVotes=votes)


    # summery:
    # Received generated key, and 2 chars representing 2 songs in playlist.
    #First char is for increment. Second char is for decrement(in case of changing the song choice).
    #For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_P_Test, Song,
                      path='voteForSongs/', http_method='GET',
                      name='voteForSongs')
    def voTunes_voteForSongs(self,
                             request):  #id format: <id-6 numbers><song-digit-for-vote-up><song-digit-for-vote-down> (digit '9' means do not vote down any song)
        id = request.id
        q = get_youtube_playlist(id)
        my_playlist = get_youtube_playlist(id)
        ps = PlaceDB(play_list=my_playlist, id="123")
        ps.put()
        hi = PlaceDB.get_by_id("123")
        return Song(name = str(hi))


APPLICATION = endpoints.api_server([voTunesApi])