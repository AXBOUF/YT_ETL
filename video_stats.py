import requests 
import os 
from dotenv import load_dotenv
import json 
from pprint import pprint

load_dotenv()
channel_handle = "bbacalhau"
API_KEY = os.getenv('API_KEY')
def summarize_json(data):
    # i  want to see the general structure of the json response and the keys that are present in it
    summary = {
        "kind": data.get("kind"),
        "etag": data.get("etag"),
        "nextPageToken": data.get("nextPageToken"),
        "items_count": len(data.get("items", [])),
        "items_keys": [item.keys() for item in data.get("items", [])]
    }
    return summary
def get_channel_playlist_id(handle):
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={handle}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        channel_items = data['items'][0]

        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        # with open ("channel.json" , "w" ) as f:
        #     json.dump(data, f, indent=4)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        return e
def count(anything): # why because i can 
    return len(anything)
def get_video_ids(playlist_id):
    '''
        { # this is the general structure of the json response that we get from the youtube api when we call the playlistItems endpoint thanks to pprint 
    'etag': 'aoY6PEvlNZMjGrJjF_o68-zDJPc',
    'items': [{'contentDetails': {'videoId': 'EIbLMyG4mkY',
                                'videoPublishedAt': '2026-04-04T11:07:25Z'},
                'etag': 'jF3OjHJ95rlPcn27OPVO13sb2rM',
                'id': 'VVVHczFKamlSQkVLTWxWRDRlVXhKMnd3LkVJYkxNeUc0bWtZ',
                'kind': 'youtube#playlistItem'}],
    'kind': 'youtube#playlistItemListResponse',
    'nextPageToken': 'EAAaHlBUOkNBRWlFRGcxT0ROQk1EaEZPRVF5UWpFeE1UQQ',
    'pageInfo': {'resultsPerPage': 1, 'totalResults': 92}
    } 
 '''

    video_ids = []
    pagetoken  = ""
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}" # & is for new parameter yo 
    try:
        while True:
            
            url = base_url 
            if pagetoken: # this means until pagetoken is empty ( while this mean page token is not emptee)
                url += f"&pageToken={pagetoken}"

            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            for item in data.get('items', []): # we have this for modularity if loop cant find items it will not thow an errior 
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            # return count(video_ids)
            #  # Check if there is a next page
            pagetoken = data.get('nextPageToken')
            if not pagetoken:
                break
        return video_ids
             
    except requests.exceptions.RequestException as e:
        return e

if __name__ == "__main__":
    # print(f"here is the playlist ID: {get_channel_playlist_id(channel_handle)}")
    playlist_id = get_channel_playlist_id(channel_handle)
    get_video_ids(playlist_id)
