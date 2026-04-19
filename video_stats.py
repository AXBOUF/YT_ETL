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
def get_channel_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"
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

# def batch_video_ids( video_ids, batch_size=50):
#     for i in range(0, len(video_ids), batch_size):
#         yield video_ids[i:i + batch_size] # wtf is yeild ? 
#         # yield is a keyword in python that is used to create a generator. 
#         # A generator is a special type of iterator that allows you to iterate over a sequence of values without having to store the entire sequence in memory at once. 
#         # When a function contains the yield keyword, it becomes a generator function. When the generator function is called, it returns a generator object that can be iterated over. 
#         # Each time the yield statement is executed, the current state of the function is saved, and the value specified by yield is returned to the caller. 

"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=EIbLMyG4mkY&key=[YOUR_API_KEY]"

def extract_video_data(video_ids):
    '''
    {
    "kind": "youtube#videoListResponse",
    "etag": "M-YUaxIgVGF0UFDkBFwh5QCc54g",
    "items": [
        {
        "kind": "youtube#video",
        "etag": "xjxGcwGI8Lgn1mVK8qY46lTv_I0",
        "id": "EIbLMyG4mkY",
        "snippet": {
            "publishedAt": "2026-04-04T11:07:25Z",
            "channelId": "UCGs1JjiRBEKMlVD4eUxJ2ww",
            "title": "Houses in Northern Norway Are Surprisingly Cheap",
            "description": "Use code BERN15 to get 15% off your Simify eSIM here: https://simify.com/bern15?c=1\n\nSubstack: https://line-on-a-map.com/\nInstagram: https://www.instagram.com/bbacalhau/\nBuy me a coffee: https://buymeacoffee.com/bbacalhau\n\n0:00 Intro  \n0:29 House Cost  \n1:35 Buying Process in Norway  \n2:28 Full Price Breakdown  \n3:30 Renovation Plans  \n4:26 Getting Internet  \n5:34 House History  \n6:25 What’s the Ladder For?  \n6:55 Plans for the Sheds  \n8:13 Why Northern Norway?  \n9:29 House Color Choice  \n10:13 Where We Found the House  \n10:38 Structural Inspection  \n11:13 House Tour  \n11:27 Hand Update",
            "thumbnails": {
            "default": {
                "url": "https://i.ytimg.com/vi/EIbLMyG4mkY/default.jpg",
                "width": 120,
                "height": 90
            },
            "medium": {
                "url": "https://i.ytimg.com/vi/EIbLMyG4mkY/mqdefault.jpg",
                "width": 320,
                "height": 180
            },
            "high": {
                "url": "https://i.ytimg.com/vi/EIbLMyG4mkY/hqdefault.jpg",
                "width": 480,
                "height": 360
            },
            "standard": {
                "url": "https://i.ytimg.com/vi/EIbLMyG4mkY/sddefault.jpg",
                "width": 640,
                "height": 480
            },
            "maxres": {
                "url": "https://i.ytimg.com/vi/EIbLMyG4mkY/maxresdefault.jpg",
                "width": 1280,
                "height": 720
            }
            },
            "channelTitle": "Bernardo Bacalhau",
            "categoryId": "22",
            "liveBroadcastContent": "none",
            "defaultLanguage": "en",
            "localized": {
            "title": "Houses in Northern Norway Are Surprisingly Cheap",
            "description": "Use code BERN15 to get 15% off your Simify eSIM here: https://simify.com/bern15?c=1\n\nSubstack: https://line-on-a-map.com/\nInstagram: https://www.instagram.com/bbacalhau/\nBuy me a coffee: https://buymeacoffee.com/bbacalhau\n\n0:00 Intro  \n0:29 House Cost  \n1:35 Buying Process in Norway  \n2:28 Full Price Breakdown  \n3:30 Renovation Plans  \n4:26 Getting Internet  \n5:34 House History  \n6:25 What’s the Ladder For?  \n6:55 Plans for the Sheds  \n8:13 Why Northern Norway?  \n9:29 House Color Choice  \n10:13 Where We Found the House  \n10:38 Structural Inspection  \n11:13 House Tour  \n11:27 Hand Update"
            },
            "defaultAudioLanguage": "en"
        },
        "contentDetails": {
            "duration": "PT13M",
            "dimension": "2d",
            "definition": "hd",
            "caption": "false",
            "licensedContent": true,
            "contentRating": {},
            "projection": "rectangular"
        },
        "statistics": {
            "viewCount": "78952",
            "likeCount": "4061",
            "favoriteCount": "0",
            "commentCount": "316"
        }
        }
    ],
    "pageInfo": {
        "totalResults": 1,
        "resultsPerPage": 1
    }
    }
    '''
    extracted_data = []
    maxResults = 50 # this is the maximum number of video ids that we can send in one API call to the videos endpoint
    def batch_video_ids(video_ids, batch_size=50):
        for i in range(0, len(video_ids), batch_size):
            yield video_ids[i:i + batch_size]

    try:
        for batch in batch_video_ids(video_ids, maxResults):
            video_ids_str = ",".join(batch) # this will convert the list of video ids into a comma separated string that we can use in the API call
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":content_details['duration'], # might need to add none in case some vid doesnot have it public
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None)
                }
                extracted_data.append(video_data)
        return extracted_data


    except requests.exceptions.RequestException as e:
        return e

if __name__ == "__main__":
    # print(f"here is the playlist ID: {get_channel_playlist_id(channel_handle)}")
    playlist_id = get_channel_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_video_data(video_ids)
    
