import requests
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"
maxResult = 50

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

def get_video_ids(playlistid):
    videos_ids=[]
    page_token = None
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlistid}&key={API_KEY}"

    try:
        while True:
            url=base_url
            if page_token:
                url+=f"&pageToken={page_token}"
            response = requests.get(url)  
            response.raise_for_status()
            data=response.json() 

            for item in data.get('items',[]):
                vid_id=item['contentDetails']['videoId']
                videos_ids.append(vid_id)
            
            page_token=data.get('nextPageToken')
            if not page_token:
                break
        
        return videos_ids

    except requests.exceptions.RequestException as e:
        raise e



def extract_video_data(videos_ids):
    extracted_data=[]

    def batch_list(video_ids_list,size):
        for vid in range (0,len(video_ids_list),size):
            yield video_ids_list[vid:vid+size]
    
    try:
        for batch in batch_list(videos_ids,maxResult):
            vid_id_str=",".join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={vid_id_str}&key={API_KEY}"
            response = requests.get(url)  
            response.raise_for_status()
            data=response.json() 

            for item in data.get('items',[]):
                video_id=item['id']
                snippet=item['snippet']
                statistics=item['statistics']
                contentDetails=item['contentDetails']

                video_data={
                    "video_id":video_id,
                    "title":snippet['title'],
                    "duration":contentDetails['duration'],
                    "publishedAt":snippet['publishedAt'],
                    "viewCount":statistics.get('viewCount',None),
                    "likeCount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None)
                }
                extracted_data.append(video_data)
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e



def save_to_json(extracted_data):
    file_path=f"./data/YT_data_{date.today()}.json"

    with open (file_path,"w",encoding="utf-8")as json_outfile:
        json.dump(extracted_data,json_outfile,indent=4,ensure_ascii=False)

if __name__=="__main__":
    playlistId=get_playlistid()
    video_ids=get_video_ids(playlistId)
    data=extract_video_data(video_ids)
    save_to_json(data)
   # print(data)

    


