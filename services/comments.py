from apiclient.discovery import build
import pandas as pd
import numpy as np

def scrape_comments_with_replies(ID):
    try:
        api_key = "AIzaSyD5nmkjStNwQ5eBd3gFtJLrdFGX0mNx23Q" 
        youtube = build('youtube', 'v3', developerKey=api_key)
        box=[]
        data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]

            box.append(comment)
            
        while ("nextPageToken" in data):

            data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                                maxResults='100', textFormat="plainText").execute()

            for i in data["items"]:
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]

                box.append(comment)      
        if(box == None):
            return []
        return box
    except Exception:
        return []