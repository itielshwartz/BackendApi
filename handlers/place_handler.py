from backend_types.playlist_types_api import Place
from backend_types.playlist_types_db import PlayListDB

__author__ = 'ishwartz'


def convert_place(currentPlace):
    generatedKey_new = ""
    number_of_song_new = -1
    loc_new = ""
    enable_new = False
    new_current_playlist = ""
    new_playlist_history = list()
    if currentPlace:
        generatedKey_new = currentPlace.key.id()
        number_of_song_new = currentPlace.size_of_play_list
        loc_new = currentPlace.loc
        enable_new = currentPlace.enable
        new_current_playlist = currentPlace.current_play_list
        history = currentPlace.play_list_history
        new_playlist_history = [PlayListDB.get_by_id(i).real_name for i in currentPlace.play_list_history]
    return Place(generatedKey=generatedKey_new, number_of_song=number_of_song_new, loc=loc_new, enable=enable_new,
                 playingPlaylist=new_current_playlist, play_list_history=new_playlist_history)