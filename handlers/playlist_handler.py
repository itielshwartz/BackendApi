import random

from google.appengine.api import memcache

from backend_types.playlist_types_api import androidPlaylist, Song
from backend_types.playlist_types_db import PlaceDB, PlayListDB
from backend_types.playlist_types_genereted import gen_playlist
from backend_types.youtube_data_wrapper import get_youtube_playlist


__author__ = 'ishwartz'


def add_playlist_to_cache(request):
    temp_playlist = generatePlaylist(request.id)
    data = memcache.get(request.id)
    if data is None:
        q = gen_playlist(request.id, temp_playlist,[])
        memcache.add(request.id, q)
    else:
        q = gen_playlist(request.id, temp_playlist, data.reg_ids)
        memcache.replace(request.id, q )
    return q


def generatePlaylist(id):
    currentPlace = PlaceDB.get_by_id(id)
    tryyoutube = PlayListDB.get_by_id(currentPlace.current_play_list)
    youtubePlaylist = currentPlace.get_current_playlist()
    songsList = []
    max_size = min(currentPlace.size_of_play_list, len(youtubePlaylist.items))
    songsNumbers = random.sample(range(len(youtubePlaylist.items)), max_size)
    for song in songsNumbers:
        songsList.append(youtubePlaylist.items[song])
    return songsList


def convert_playlist(playlist, songs):
    csongs = androidPlaylist()
    i = 0
    for song in playlist:
        csongs.songs.append(Song(votes=songs[i], name=song.name, youtubeUrl=song.id,pos=0))
        i += 1
    return csongs


def add_playlistDB(playlist_id):
    playlist = PlayListDB.get_by_id(playlist_id)
    if playlist is None:
        playlist = get_youtube_playlist(playlist_id)
        playlist.put()
