import json
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
#import cv2
import os
import time
import pytesseract
from pytesseract import Output
from PIL import Image
from apiclient.discovery import build
import argparse
import unidecode
import pandas as pd
import urllib
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 

from .services import comments
from .services import relative_score

DEVELOPER_KEY="AIzaSyD5nmkjStNwQ5eBd3gFtJLrdFGX0mNx23Q"
YOUTUBE_API_SERVICES_NAME="youtube"
YOUTUBE_API_VERSION="v3"
titles=[]
PublishTime=[]
videoIds=[]
channelTitles=[]
channelId=[]
video_descriptions=[]


viewCounts=[]
likeCounts=[]
dislikeCounts=[]
commentCounts=[]
duration=[]
favoritesCounts=[]
URLS=[]
Audience_Response=[]

def getCaptions(url):
  try:
    srt = YouTubeTranscriptApi.get_transcript(url,languages=['en'])
    ans=""
    for i in srt:
      ans=ans+" "+i['text']
    return ans
  except Exception:
    return ""


def getVideo(URL):
    try: 
        yt = YouTube(URL)
        #print(yt)
        stream = yt.streams.get_highest_resolution()
        #print(stream)
        srt=stream.download()
        #print(srt)
        #print("Download completed!!")
        return srt
    except Exception:
        return ""

def getDuration(URL):
    YT_KEY="AIzaSyD5nmkjStNwQ5eBd3gFtJLrdFGX0mNx23Q"# API key
    search_url = f'https://www.googleapis.com/youtube/v3/videos?id={URL}&key={YT_KEY}&part=contentDetails'
    req = urllib.request.Request(search_url)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    all_data = data['items']
    duration = all_data[0]['contentDetails']['duration']
    #print(duration)
    minutes=0
    if('H' in duration):
        minutes = int(duration[2:].split('H')[0])*60
        duration=duration[0:2]+duration.split('H')[1]
        #print(duration)
    if('M' in duration):
        minutes =minutes+ int(duration[2:].split('M')[0])
        return minutes
    return 0
'''
def get_frames(URL,step,count):

  # Input:
  #   URL - url of video
  #   outputFolder - name and path of the folder to save the results
  #   step - time lapse between each step (in seconds)
  #   count - number of screenshots
  # Output:
  #   'count' number of screenshots that are 'step' seconds apart created from video 'inputFile' and stored in folder 'outputFolder'
  # Function Call:
  #   get_frames("test.mp4", 'data', 10, 10)
  inputFile=getVideo(URL)
  if(inputFile==""):
    return ""
  #initializing local variables
  step = step
  frames_count = count

  currentframe = 0
  frames_captured = 0

  #creating a folder
  try:  
      # creating a folder named data 
      if not os.path.exists("/data/"): 
          os.makedirs("/data/") 
    
  #if not created then raise error 
  except OSError: 
      print ('Error! Could not create a directory') 
      return
  
  cam = cv2.VideoCapture(inputFile)
  #reading the number of frames at that particular second
  frame_per_second = cam.get(cv2.CAP_PROP_FPS)
  words =""
  while (True):
      ret, frame = cam.read()
      if ret:
          if currentframe > (step*frame_per_second):  
              currentframe = 0
              #saving the frames (screenshots)
              #name = './data/frame' + str(frames_captured) + '.jpg'
              #print ('Creating...' + name) 
              #cv2_imshow(frame)  

              #print ('getting text...' + name) 
              # pytessercat
              text = pytesseract.image_to_string(frame)
              #print(text)
              words=words+" "+text

              #cv2.imwrite(name, frame)       
              frames_captured+=1
              
              #breaking the loop when count achieved
              if frames_captured > frames_count-1:
                ret = False
          currentframe += 1           
      if ret == False:
          break
  cam.release()
  os.remove(inputFile)
  special_characters = ['!','#','$','%', '&','@','[',']',' ',']','_','-','=','+','?','|','\n','\x0c']
  words = ''.join(filter(lambda i:i not in special_characters, words))

  return words
'''
def youtube_mobie_review(x,max_Results):
    youtube=build(YOUTUBE_API_SERVICES_NAME,YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    #print("get connection")
    #print(youtube)
    iterator=0
    token=""
    while(iterator< max_Results ):
      iterator=iterator+50
      search_response=youtube.search().list(q=x, part="id,snippet",maxResults=max_Results,pageToken=token).execute()
      #print("get search results")
      #print(search_response)
      token=search_response["nextPageToken"]
      df=pd.DataFrame()
      count=0
      for search_result in search_response.get("items",[]):
          count=count+1
          #print(count)
          if search_result["id"]["kind"]=="youtube#video":
              #print(search_result["snippet"])
              title=search_result["snippet"]["title"]
              title=unidecode.unidecode(title)
              titles.append(title.lower())
              #print("Title : "+title)
              
              publishedAt=search_result["snippet"]["publishedAt"]
              PublishTime.append(publishedAt)
              #print("publishedAt : "+str(publishedAt))
              
              channelTitle=search_result["snippet"]["channelTitle"]
              channelTitles.append(channelTitle)
              #print("channel name : "+str(channelTitle))
            #   Channel_Id=search_result["snippet"]["channelId"]
            #   channelId.append(Channel_Id)
              
              videoId=search_result["id"]["videoId"]
              videoIds.append(videoId)
              #print("videoId : "+str(videoId))
              
              url="https://www.youtube.com/watch?v="+videoId
              URLS.append(url)
              
              video_description=search_result["snippet"]["description"]
              video_descriptions.append(video_description.lower())
              #print("Description : "+str(video_description))
              
              video_response=youtube.videos().list(id=videoId,part="statistics").execute()
              
              for video_result in video_response.get("items",[]):
                  viewCount=video_result["statistics"]["viewCount"]
                  viewCounts.append(viewCount)
                  
                  if 'likeCount' not in video_result['statistics']:
                      likeCount=0
                  else:
                      likeCount=video_result["statistics"]["likeCount"]
                  likeCounts.append(likeCount)
                  
                  if 'commentCount' not in video_result['statistics']:
                      commentCount=0
                  else:
                      commentCount=video_result["statistics"]["commentCount"]
                  commentCounts.append(commentCount)
              duration.append(getDuration(videoId))
              
              dict1={"Title":titles,"PublishTime":PublishTime,"URL":URLS,"Channel_Name":channelTitles,"Description":video_descriptions,"viewCount":viewCounts,"commentCount":commentCounts,"likeCount":likeCounts,"Duration":duration}
              
              df=pd.DataFrame.from_dict(dict1,orient='index')
              df=df.transpose()
              df.columns=['Title','PublishTime','URL','Channel_Name','Description','viewCount','commentCount','likeCount',"Duration"]
            
            
    #print(count)
    return df

def key_words(x,max_Result):
    print("getting new data from api....")
    youtube_response_df=youtube_mobie_review(x,max_Result)
    youtube_response_df=youtube_response_df.dropna()
    youtube_response_df['relative_score']=0
    #youtube_response_df['video_text']=''
    for i in range(youtube_response_df.shape[0]):
        print(str(i))
        URL = youtube_response_df.at[i, "URL"]
        URL=URL[URL.index("=")+1:]
        # print(URL)
        youtube_response_df.at[i, "relative_score"]= relative_score.get_relative_score(x,youtube_response_df.loc[i], getCaptions(URL).lower() )  # audio
        #youtube_response_df.at[i, "video_text"]= get_frames(youtube_response_df.at[i, "URL"],3,100)   # video
    youtube_response_df.sort_values(by=['relative_score'], ascending=False)
    print("we sorted the data ..... ")
    return youtube_response_df[:50]


    