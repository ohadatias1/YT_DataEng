import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"

def get_playlistid():
    try:
        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data=response.json()
        json.dumps(data,indent=4)   #store it as json
        channel_items=data['items'][0]
        channel_playlistID = channel_items['contentDetails']['relatedPlaylists']['uploads'] #the id of the videos
        print(channel_playlistID)
        return channel_playlistID
    except requests.exceptions.RequestException as e:
        raise e

if __name__=="__main__":
    get_playlistid()
    


