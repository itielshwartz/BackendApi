from backend_types.playlist_types_db import PlayListDB, SongDB

__author__ = 'ishwartz'

from apiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyDkxAhehyf2mH83JfjhzagmvEYEs_A17_k'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
#
# def getVideoLength(id):
# time = ""
# youtube_1 = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#     video_response = youtube_1.videos().list(id=id, part='contentDetails, recordingDetails').execute()
#     for video_result in video_response.get("items", []):
#         time = video_result["contentDetails"]["duration"]
#     return time


def get_youtube_playlist(playlist_id):
    youtube_1 = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    playlistitems_list_request = youtube_1.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=50
    )
    items = []
    i = 0
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()
        # Print information about each video.
        for playlist_item in playlistitems_list_response["items"]:
            title = playlist_item["snippet"]["title"]
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            items.append(SongDB(id=video_id, name=title, length="", pos=i))
            i += 1
        playlistitems_list_request = youtube_1.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)
    current_play_list = PlayListDB(items=items, id=playlist_id)
    return current_play_list