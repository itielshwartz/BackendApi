"""Hello World API implemented using Google Cloud Endpoints.
Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import random
import time

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from PlayListStub import playlistIdToName



# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
from types.playlist_types_db import Place, PlaceDB, Song, androidPlaylist

WEB_CLIENT_ID = '572283433642-27216moiovs3calv9clvqtimsqmldi2e.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

#package = 'Hello'

DEFAULT_PLAYLIST_SIZE = 7
PLAYLIST_ORIGINAL_SIZE = 11




def generateAndroidPlaylist():
    genList=[0 for _ in xrange(DEFAULT_PLAYLIST_SIZE)]
    i = 0
    while i < DEFAULT_PLAYLIST_SIZE:
        r=random.randint(0, PLAYLIST_ORIGINAL_SIZE-1)
        if r not in genList:
            genList[i] = r
            i+=1
    songslist = []*DEFAULT_PLAYLIST_SIZE
    for i in xrange(DEFAULT_PLAYLIST_SIZE):
        songslist.append(Song(pos = genList[i], name = playlistIdToName[genList[i]]))
    genPlaylist = androidPlaylist(songs=songslist)
    return genPlaylist

@endpoints.api(name='voTunes', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, 'endpoints.API_EXPLORER_CLIENT_ID'],
               audiences=[ANDROID_AUDIENCE])
class voTunesApi(remote.Service):

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    #summery:
    #Returns the next song to be played(max votes) in accordance with received key.
    @endpoints.method(ID_RESOURCE, Song,
                      path='getNextSongId/{id}', http_method='GET',
                      name='getNextSongId')
    def voTunes_getNextSong(self, request):
            key = int(request.id[0:6])
            currentPlace = PlaceDB.query(PlaceDB.place.generatedKey == key).get()
            m = currentPlace.place.currentVotes.index(max(currentPlace.place.currentVotes))
            print('max votes is for song num. ' + str(m))

            #generate new list and initialize votes
            #currentPlace.place.currentVotes = [0 for _ in xrange(DEFAULT_PLAYLIST_SIZE)]
            #currentPlace.place.playingPlaylist = generateAndroidPlaylist()
            #currentPlace.put()
            return Song(pos=m)

    ID_RESOURCE_S = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    #summery:
    #Returns the current playlist in accordance with received key.
    @endpoints.method(ID_RESOURCE_S, androidPlaylist,
                      path='getListOfSongs/{id}', http_method='GET',
                      name='getListOfSongs')
    def voTunes_getListOfSongs(self, request):
        key = int(request.id[0:6])
        currentPlace = PlaceDB.query(PlaceDB.place.generatedKey == key).fetch(1)
        return currentPlace[0].place.playingPlaylist

    ID_RESOURCE_UserId = endpoints.ResourceContainer(
        message_types.VoidMessage,
        userKey=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE_UserId, Song,
                      path='getUserKey/{userKey}', http_method='GET',
                      name='getUserKey')
    def voTunes_getUserKey(self, request):
        try:
            return Song(pos=request.userKey)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    ID_RESOURCE_P = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    #summery:
    #Received generated key and creates an entity in the DB as a new place
    @endpoints.method(ID_RESOURCE_P, Song,
                      path='getPlaylistandUserKey/{id}', http_method='GET',
                      name='getPlaylistandUserKey')
    def voTunes_getPlaylistandUserKey(self, request):
        genKey = int(request.id[0:6])
        my_place = Place(generatedKey=genKey, playingPlaylist=generateAndroidPlaylist(), currentVotes=[0 for _ in xrange(DEFAULT_PLAYLIST_SIZE)]) # place object with new generated playlist and initialized votes list
        ps = PlaceDB(place=my_place, name='MyPubs') #creates the entity
        #key = ps.put() #adding place to DB

        time.sleep(2) #time for DB to get updated

        new_places = PlaceDB.query().fetch()
        print('####################################')
        print('new_places = ' + str(new_places))
        print('####################################')
        return Song(name=str(new_places))

    #summery:
    #Received generated key, and 2 chars representing 2 songs in playlist.
    #First char is for increment. Second char is for decrement(in case of changing the song choice).
    #For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_P, Place,
                      path='voteForSong/{id}', http_method='GET',
                      name='voteForSong')
    def voTunes_voteForSong(self, request): #id format: <id-6 numbers><song-digit-for-vote-up><song-digit-for-vote-down> (digit '9' means do not vote down any song)
        key = int(request.id[0:6])
        voteUp = request.id[6:7]
        voteDown = request.id[7:8]
        currentPlace = PlaceDB.query(PlaceDB.place.generatedKey == key).get()
        if voteUp == 'O' and voteDown == 'O': #initialize the votes - for debug
            for i in xrange(DEFAULT_PLAYLIST_SIZE):
                 currentPlace.place.currentVotes[i] = 0
        if voteUp != 'I':
            currentPlace.place.currentVotes[int(voteUp)] += 1
        if voteDown != 'I':
            currentPlace.place.currentVotes[int(voteDown)] -= 1
        currentPlace.put()
        time.sleep(2)
        return Place(currentVotes = currentPlace.place.currentVotes)


    # @endpoints.method(message_types.VoidMessage, SongsCollection,
    #                   path='AllList/{id}', http_method='GET',
    #                   name='ListAll')
    # def greetings_list_1(self, unused_request):
    #     global current_play_list_votes
    #     global current_songs_index
    #     return SongsCollection(
    #         songs=
    #                 [SongForAndroid(name=playlistIdToName.get(current_songs_index[0]) + str(current_play_list_votes[0])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[1]) + str(current_play_list_votes[1])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[2]) + str(current_play_list_votes[2])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[3]) + str(current_play_list_votes[3])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[4]) + str(current_play_list_votes[4])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[5]) + str(current_play_list_votes[5])),
    #                SongForAndroid(name=playlistIdToName.get(current_songs_index[6]) + str(current_play_list_votes[6]))])

APPLICATION = endpoints.api_server([voTunesApi])