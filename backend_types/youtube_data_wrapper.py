from backend_types.playlist_types_db import PlayList, Song

__author__ = 'ishwartz'

from apiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyCZ7p97PFGdwD-3DVW6AVtR-t_5m-Uo3XM'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def getVideoLength(id):
    time = ""
    youtube_1 = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    video_response = youtube_1.videos().list(id=id, part='contentDetails, recordingDetails').execute()
    for video_result in video_response.get("items", []):
        time = video_result["contentDetails"]["duration"]
    return time


def get(playlist_id):
    youtube_1 = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    playlistitems_list_request = youtube_1.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=50
    )
    items = []
    current_play_list = PlayList(playlist_id, items)
    while playlistitems_list_request:
        playlistitems_list_response = playlistitems_list_request.execute()
        # Print information about each video.
        for playlist_item in playlistitems_list_response["items"]:
            title = playlist_item["snippet"]["title"]
            video_id = playlist_item["snippet"]["resourceId"]["videoId"]
            items.append(Song(video_id, title, str(getVideoLength(video_id))))
        playlistitems_list_request = youtube_1.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)
    return current_play_list