"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from random import randint



# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'

playlistOfOwners = dict()


playlist = {0: "Muse - Feeling Good", 1: "Muse - New Born", 2: "Muse - Unintended", 
3: "Muse - Bliss", 4: "Muse - Plug In Baby", 5: "Muse - Uprising", 6: "Muse - Knights Of Cydonia", 
7: "Muse - Starlight", 8: "Muse - Invincible", 9: "Muse - Sunburn", 10: "Muse - Hysteria"}

playlistOP = {"Muse - Feeling Good" : 0, "Muse - New Born" : 1, "Muse - Unintended" : 2, 
"Muse - Bliss" : 3, "Muse - Plug In Baby" : 4, "Muse - Uprising" : 5, "Muse - Knights Of Cydonia" : 6, 
"Muse - Starlight" : 7, "Muse - Invincible" : 8, "Muse - Sunburn" : 9, "Muse - Hysteria" : 10}

#playlistVotes = {"Muse - Feeling Good" : 0, "Muse - New Born" : 0, "Muse - Unintended" : 0, 
#"Muse - Bliss" : 0, "Muse - Plug In Baby" : 0, "Muse - Uprising" : 0, "Muse - Knights Of Cydonia" : 0, 
#"Muse - Starlight" : 0, "Muse - Invincible" : 0, "Muse - Sunburn" : 0, "Muse - Hysteria" : 0}
playlistVotes = list()


class GeneratedSongs:
    @staticmethod
    def generateSong(numOfSongs):
        selectedSongs = list()
        selectedSet = set()
        i = 0
        while i < 7:
            rand = randint(0,10)
            song = playlist[rand]
            if song not in selectedSet:
                selectedSongs.append(song)
                selectedSet.add(song)
                i+=1
        return selectedSongs

class SongId(messages.Message):
    """Greeting that stores a message."""
    id = messages.IntegerField(1)

class SongForAndroid(messages.Message):
    """Greeting that stores a message."""
    name = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(SongId, 1, repeated=True)


class SongsCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(SongForAndroid, 1, repeated=True)
        

STORED_GREETINGS = GreetingCollection(items=[
    SongId(id=0),
    SongId(id=3),
])

STORED_SONGS = SongsCollection(items=[
    SongForAndroid(name="Hi avia this is the first song!"),
    SongForAndroid(name="Hi avia this is the Second song!"),
    SongForAndroid(name="Hi avia this is the Third song!"),
    SongForAndroid(name="Hi avia this is the 4 song!"),
    SongForAndroid(name="Hi avia this is the V song!"),
    SongForAndroid(name="Hi avia this is the also a song!"),
    SongForAndroid(name="Hi avia this is the Last Song!!!! if you can read this - wow!!!"),

])


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, 'endpoints.API_EXPLORER_CLIENT_ID'],
               audiences=[ANDROID_AUDIENCE])
class HelloWorldApi(remote.Service):

    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, SongId,
                      path='getSongId/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            #return STORED_GREETINGS.items[request.id]
            m = max(playlistVotes)
            for i in range(0,11):
                playlistVotes[i]=0
            return SongId(id=m)
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))


    @endpoints.method(message_types.VoidMessage, SongsCollection,
                      path='getSongPlease', http_method='GET',
                      name='getSongs.list')
    def greetings_list(self, unused_request):
        selectedSongs = GeneratedSongs.generateSong(7)
        return SongsCollection(items=[SongForAndroid(name=selectedSongs[0]),
                                    SongForAndroid(name=selectedSongs[1]),
                                    SongForAndroid(name=selectedSongs[2]),
                                    SongForAndroid(name=selectedSongs[3]),
                                    SongForAndroid(name=selectedSongs[4]),
                                    SongForAndroid(name=selectedSongs[5]),
                                    SongForAndroid(name=selectedSongs[6])])

    
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
        i = 0
        for i in range(0,11):
            playlistVotes.append(0)
        playlistOfOwners[request.id[0:6]] = request.id[6:]
        return SongForAndroid(name=playlistOfOwners[request.id[0:6]])


    @endpoints.method(ID_RESOURCE_P, SongForAndroid,
                      path='getVote/{id}', http_method='GET',
                      name='getVote')
    def greetings_get_vote(self, request):  
        playlistVotes[playlist[request.id]] += 1
        return SongForAndroid(name=str(playlistVotes))


APPLICATION = endpoints.api_server([HelloWorldApi])
