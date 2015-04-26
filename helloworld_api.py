"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'


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
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))


    @endpoints.method(message_types.VoidMessage, SongsCollection,
                      path='getSongPlease', http_method='GET',
                      name='getSongs.list')
    def greetings_list(self, unused_request):
        return STORED_SONGS

APPLICATION = endpoints.api_server([HelloWorldApi])
