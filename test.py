from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import cv2
import os
import time
import pytesseract
from pytesseract import Output
from PIL import Image
from apiclient.discovery import build
import argparse
import unidecode
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 
def getVideo(URL):
  yt = YouTube(URL)
  #print(yt)
  stream = yt.streams.get_highest_resolution()
  #print(stream)
  srt=stream.download()
  #print(srt)
  #print("Download completed!!")
  return srt
def get_frames(URL,step,count):

  '''
  Input:
    URL - url of video
    outputFolder - name and path of the folder to save the results
    step - time lapse between each step (in seconds)
    count - number of screenshots
  Output:
    'count' number of screenshots that are 'step' seconds apart created from video 'inputFile' and stored in folder 'outputFolder'
  Function Call:
    get_frames("test.mp4", 'data', 10, 10)
  '''
  inputFile=getVideo(URL)
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


words= get_frames("https://www.youtube.com/watch?v=00DRsxH-im8",3,10)
print(words)