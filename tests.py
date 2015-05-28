import random

from backend_types.playlist_types_db import SongDB
from backend_types.playlist_types_genereted import all_gen_playlist


__author__ = 'ishwartz'

play_list_ids = [z for z in range(0, 11)]
current_songs_index = random.sample(play_list_ids, 7)
print(play_list_ids)
print(current_songs_index)

current_playlists = all_gen_playlist()
songs = []
songs.append(SongDB(pos=0, name="name_1"))
songs.append(SongDB(pos=1, name="name_2"))
current_playlists.add_playlist("123", songs)
new_songs = [i for i in songs]
new_songs.append(SongDB(pos=3, name="name_3"))
current_playlists.add_playlist("1234", new_songs)

print(current_playlists.get_current_songs("123"))
print(current_playlists.add_vote("123", 0))
print(current_playlists.add_vote("123", 0))
print(current_playlists.get_max_vote("123"))
print(current_playlists.get_current_songs("1234"))