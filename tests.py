import random

__author__ = 'ishwartz'

play_list_ids= [z for z in range(0,11)]
current_songs_index = random.sample(play_list_ids, 7)
print(play_list_ids)
print(current_songs_index)