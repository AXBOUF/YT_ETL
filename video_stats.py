import requests 
import os 
from dotenv import load_dotenv
import json 

load_dotenv()
channel_handle = "bbacalhau"

def get_channel_playlist_id(handle):
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={handle}&key={os.getenv('API_KEY')}"
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
        

if __name__ == "__main__":
    print(get_channel_playlist_id(channel_handle))
