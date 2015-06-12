import endpoints
from protorpc import remote
from google.appengine.api import memcache


# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
from Utilities import sendMessageToClients
from backend_types.playlist_types_api import Place, Song, androidPlaylist
from backend_types.playlist_types_db import PlaceDB
from backend_types.playlist_types_genereted import gen_playlist
from backend_types.request_types import ID_RESOURCE, ID_RESOURCE_S, ID_RESOURCE_P_Test, ID_RESOURCE_SETTING, \
    ID_RESOURCE_P, ID_RESOURCE_R
from handlers.place_handler import convert_place
from handlers.playlist_handler import add_playlist_to_cache, generatePlaylist, convert_playlist, add_playlistDB

WEB_CLIENT_ID = '572283433642-27216moiovs3calv9clvqtimsqmldi2e.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


@endpoints.api(name='voTunes', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, 'endpoints.API_EXPLORER_CLIENT_ID'],
               audiences=[ANDROID_AUDIENCE])
class voTunesApi(remote.Service):
    @endpoints.method(ID_RESOURCE, Place,
                      path='checkForPlaylist/{id}', http_method='GET',
                      name='checkForPlaylist')
    def voTunes_checkForPlaylist(self, request):
        currentPlace = PlaceDB.get_by_id(request.id)
        return convert_place(currentPlace)

    # summery:
    # Returns the next song to be played(max votes) in accordance with received key.
    @endpoints.method(ID_RESOURCE, Song,
                      path='getNextSongId/{id}', http_method='GET',
                      name='getNextSongId')
    def voTunes_getNextSong(self, request):
        currentPlace = memcache.get(request.id).get_max_song()
        temp_playlist = generatePlaylist(request.id)
        q = gen_playlist(request.id, temp_playlist)
        memcache.replace(request.id, q)
        # to do add genreted
        return Song(pos=currentPlace.pos)

    # summery: updates regIDs of a place with a new regID
    @endpoints.method(ID_RESOURCE_R, Place,
                      path='sendRegId/', http_method='GET',
                      name='sendRegId')
    def voTunes_sendRegId(self, request):
        current_reg_ids = memcache.get(request.id).reg_ids
        current_reg_ids.append(request.reg_id)
        votes = memcache.get(request.id).votes
        return Place(currentVotes=votes)


    # summery:
    # Returns the current playlist in accordance with received key.
    @endpoints.method(ID_RESOURCE_S, androidPlaylist,
                      path='getListOfSongs/{id}', http_method='GET',
                      name='getListOfSongs')
    def voTunes_getListOfSongs(self, request):
        playlist = memcache.get(request.id)
        songs = playlist.songs
        votes = playlist.votes
        msg_playlist = convert_playlist(songs, votes)
        return msg_playlist

    # summery:
    # Received generated key and creates an entity in the DB as a new place

    @endpoints.method(ID_RESOURCE_P, androidPlaylist,
                      path='addPlaylistandUserKey/', http_method='GET',
                      name='addPlaylistandUserKey')
    def voTunes_addPlaylistandUserKey(self, request):
        add_playlistDB(request.play_list_id)
        place = PlaceDB.get_by_id(request.id)
        curr_playlist = ""
        new_playlist_history = set()
        if place is not None:
            curr_playlist = place.get_current_playlist()
            new_playlist_history = {i for i in place.play_list_history}
        new_playlist_history.add(request.play_list_id)
        db_playlist_history = sorted([i for i in new_playlist_history])
        ps = PlaceDB(current_play_list=request.play_list_id, id=request.id, play_list_history=db_playlist_history)
        ps.put()
        temp_playlist = add_playlist_to_cache(request)
        android_playlist = convert_playlist(temp_playlist.songs, temp_playlist.votes)
        return android_playlist

    # summery:
    # Received generated key, and 2 chars representing 2 songs in playlist.
    # First char is for increment. Second char is for decrement(in case of changing the song choice).
    # For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_P_Test, androidPlaylist,
                      path='voteForSong/', http_method='GET',
                      name='voteForSong')
    def voTunes_voteForSong(self, request):
        id = request.id
        up = request.up
        down = request.down
        playlist = memcache.get(request.id)
        if (down is not None):
            playlist.votes[down] -= 1
        if up is not None:
            playlist.votes[up] += 1
        memcache.replace(id, playlist)
        android_playlist = convert_playlist(playlist.songs, playlist.votes)
        reg_ids = memcache.get(request.id).reg_ids
        if (len(reg_ids) > 0):
            sendMessageToClients(messageType = 'Votes-Updated',registration_ids = reg_ids ,data=android_playlist)

        return android_playlist

    # summery:
    # Received generated key, and 2 chars representing 2 songs in playlist.
    # First char is for increment. Second char is for decrement(in case of changing the song choice).
    # For both chars - 'I' represents ignore choice.
    @endpoints.method(ID_RESOURCE_SETTING, Place,
                      path='updatePlaceSetting/', http_method='GET',
                      name='updatePlaceSetting')
    def voTunes_updateSetting(self, request):
        id = request.id
        new_place = PlaceDB.get_by_id(id)
        new_size = request.play_list_size
        new_enable = request.enable
        new_loc = request.loc
        if new_size is not None:
            setattr(new_place, 'size_of_play_list', new_size)
        if new_enable is not None:
            setattr(new_place, 'enable', new_enable)
        if new_loc is not None:
            setattr(new_place, 'loc', new_loc)
        new_place.put()
        return convert_place(PlaceDB.get_by_id(id))
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


APPLICATION = endpoints.api_server([voTunesApi])