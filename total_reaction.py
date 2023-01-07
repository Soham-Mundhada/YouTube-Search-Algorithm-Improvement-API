import json
import pandas as pd
from apiclient.discovery import build

def get_normalized_intrested_audiance(data):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey="AIzaSyAfFM-ZlbVD-E5392Yd5jcO2CBZbkvzo2g")
    normalized_intrested_audiance_ratio=0
    for index, row in data.iterrows():
        request = youtube.channels().list(
            part="statistics",
            id=row['Channel_Id'],
        )
        response = request.execute()
        normalized_intrested_audiance_ratio =(normalized_intrested_audiance_ratio + (int(response["items"][0]["subscriberCount"]) / int(row["viewCount"])))
    return normalized_intrested_audiance_ratio/50


def convert_dataframe(data):
    print("type of data is ---------------------------------------- "+str(type(data)))
    pdata=pd.DataFrame.from_dict(data)
    for index, row in pdata.iterrows():
        row["viewCount"]=int(row["viewCount"])
        row["commentCount"]=int(row["commentCount"])
        row["likeCount"]=int(row["likeCount"])
        row["positivenum"]=int(row["positivenum"])
        row["negativenum"]=int(row["negativenum"])
        row["neutralnum"]=int(row["neutralnum"])
    return pdata

def get_mode(pos,neg,neu):
    if(pos >= (neg + neu)):
        if(neu >= neg):
            return "Very Happy"
        if(neu < neg):
            if((2*(neg+neu))<pos):
                return "Very Happy"
            else:
                return "Mixed (More Happy)"
    
    if(neg >= (pos + neu)):
        if(neu >= pos):
            return "Very Upset"
        if(neu < pos):
            if((2*(pos+neu))<neg):
                return "Very Upset"
            else:
                return "Mixed (More Upset)"

    if(neu >= (pos + neg)):
        if(pos < neg):
            if((1.5*pos) >= neg):
                return "Neutral"
        if(pos >= neg):
            if((1.5 * neg) >= pos):
                return "Neutral"

    if(pos >= neu):
        if(neu >= neg):
            return "Happy"
        else:
            return "Mixed(More Happy)"

    if(neg >= neu):
        if(neu >= pos):
            return "Upset"
        else:
            return "Mixed(More Upset)"

    if(neu >= pos and pos >= neu):
        return "Interested"
    
    if(neu >=  neg and neg >= pos):
        return "Not Interested"

    return "Neutral"
    
 


def get_total_reaction(data):
    print("we are getting comman sentiments ---------")
    pdata=convert_dataframe(data)
    total_views=0
    for ind,row in pdata.iterrows():
        total_views += int(row['viewCount'])
    print(type(total_views))
    average_views=total_views/50
    average_comments=0
    average_likes=0
    positive =0
    negative=0
    neutral=0

    for index, row in pdata.iterrows():
        positive+=(int(row['positivenum'])*(int(row['viewCount'])/total_views))
        negative+=(int(row['negativenum'])*(int(row['viewCount'])/total_views))
        neutral+=(int(row['neutralnum'])*(int(row['viewCount'])/total_views))
        average_comments+=(int(row['commentCount'])*(int(row['viewCount'])/total_views))
        average_likes+=(int(row['likeCount'])*(int(row['viewCount'])/total_views))
    
    mode=get_mode(positive,negative,neutral)
    views_per_1000=0#get_normalized_intrested_audiance(pdata)*1000

    return positive,neutral,negative,average_views,average_likes/50,average_comments/50,mode,views_per_1000
    