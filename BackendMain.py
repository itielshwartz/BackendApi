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

WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Hello'

playlistOfOwners = dict()



# playlistVotes = {"Muse - Feeling Good" : 0, "Muse - New Born" : 0, "Muse - Unintended" : 0,
# "Muse - Bliss" : 0, "Muse - Plug In Baby" : 0, "Muse - Uprising" : 0, "Muse - Knights Of Cydonia" : 0,
#"Muse - Starlight" : 0, "Muse - Invincible" : 0, "Muse - Sunburn" : 0, "Muse - Hysteria" : 0}



class SongId(messages.Message):
    """Greeting that stores a message."""
    id = messages.IntegerField(1)


class SongForAndroid(messages.Message):
    """Greeting that stores a message."""
    name = messages.StringField(1)


class SongsCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(SongForAndroid, 1, repeated=True)


play_list_ids= [z for z in range(0,11)]


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, 'endpoints.API_EXPLORER_CLIENT_ID'],
               audiences=[ANDROID_AUDIENCE])
class HelloWorldApi(remote.Service):
    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))
    current_songs_index = []
    current_play_list_votes = []

    @endpoints.method(ID_RESOURCE, SongId,
                      path='getSongId/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            print(current_songs_index)
            m = current_songs_index[current_play_list_votes.index(max(current_play_list_votes))]
            return SongId(id=m)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))


    @endpoints.method(message_types.VoidMessage, SongsCollection,
                      path='getListOfSongs', http_method='GET',
                      name='getListOfSongs.list')
    def greetings_list(self, unused_request):
        global current_play_list_votes
        global current_songs_index
        current_songs_index = random.sample(play_list_ids, 7)
        current_play_list_votes = [0 for j in xrange(7)]
        return SongsCollection(items=[SongForAndroid(name=playlistIdToName.get(current_songs_index[0])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[1])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[2])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[3])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[4])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[5])),
                                      SongForAndroid(name=playlistIdToName.get(current_songs_index[6]))])


    ID_RESOURCE_UserId = endpoints.ResourceContainer(
        message_types.VoidMessage,
        userKey=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE_UserId, SongId,
                      path='getUserKey/{userKey}', http_method='GET',
                      name='greetings.getUserKey')
    def greeting_get_key(self, request):
        try:
            return SongId(id=request.userKey)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    ID_RESOURCE_P = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.StringField(1))

    @endpoints.method(ID_RESOURCE_P, SongForAndroid,
                      path='getPlaylistandUserKey/{id}', http_method='GET',
                      name='greetings.getPlaylistandUserKey')
    def greeting_get_playlistkey(self, request):
        global current_play_list_votes
        current_play_list_votes = [0 for j in xrange(7)]
        playlistOfOwners[request.id[0:6]] = request.id[6:]
        return SongForAndroid(name=playlistOfOwners[request.id[0:6]])


    @endpoints.method(ID_RESOURCE_P, SongForAndroid,
                      path='voteForSong/{id}', http_method='GET',
                      name='voteForSong')
    def greetings_get_vote(self, request):
        new_id = int(request.id)
        current_play_list_votes[new_id] += 1
        print(current_play_list_votes)
        return SongForAndroid(name=str(playlistIdToName[current_songs_index[new_id]]))

    @endpoints.method(message_types.VoidMessage, SongsCollection,
                      path='AllList/{id}', http_method='GET',
                      name='ListAll')
    def greetings_list_1(self, unused_request):
        global current_play_list_votes
        global current_songs_index
        return SongsCollection(
            items=
                    [SongForAndroid(name=playlistIdToName.get(current_songs_index[0]) + str(current_play_list_votes[0])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[1]) + str(current_play_list_votes[1])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[2]) + str(current_play_list_votes[2])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[3]) + str(current_play_list_votes[3])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[4]) + str(current_play_list_votes[4])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[5]) + str(current_play_list_votes[5])),
                   SongForAndroid(name=playlistIdToName.get(current_songs_index[6]) + str(current_play_list_votes[6]))])

APPLICATION = endpoints.api_server([HelloWorldApi])
