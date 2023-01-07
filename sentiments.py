from googletrans import Translator
from deep_translator import GoogleTranslator
import nltk
import re
from cleantext import clean
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .services import comments

nltk.download('punkt')
nltk.download('stopwords')
translator = Translator()
stop_words = set(stopwords.words('english'))

def clean_text(comment_arr):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    for i in range(len(comment_arr)):
        text=comment_arr[i]
        text = GoogleTranslator(source='auto', target='en').translate(text)
        text=emoji_pattern.sub(r'', text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r'\d+', '', text)
        # tokenizing each text
        text = word_tokenize(text)
        clean_text = []
        for word in text:
            clean_text.append("".join([z for z in word if z.isalnum()]))
        text_with_no_stop_word = [w.lower() for w in clean_text if not w in stop_words]
        comment_arr[i]=" ".join(" ".join(text_with_no_stop_word).split())
    
    return comment_arr

def get_Analysis(comment_arr):
    count=0
    fresult= {"positivenum":0,"negativenum":0,"neutralnum":0}
    commentbot = SentimentIntensityAnalyzer()
    for comment in comment_arr:
        vs = commentbot.polarity_scores(comment)
        count += 1
        if vs['compound']>= 0.05:
            fresult["positivenum"] +=1
        elif vs['compound']<= - 0.05:
            fresult["negativenum"] += 1
        else:
            fresult["neutralnum"] += 1
    return fresult
#data is the dataframe containing info about the 50 videos returned from API
def get_all_Sentiments(data):
    print("getteing all sentiments ...... ")
    data["positivenum"]=0
    data["negativenum"]=0
    data["neutralnum"]=0
    for i in range(data.shape[0]):
        print("sentiment of "+str(i))
        URL = data.at[i, "URL"]
        URL=URL[URL.index("=")+1:]
        #URL contains the video ID
        #print(URL)
        sentiments=get_Analysis(comments.scrape_comments_with_replies( URL))
        data.at[i, "positivenum"]=sentiments["positivenum"]
        data.at[i, "negativenum"]=sentiments["negativenum"]
        data.at[i, "neutralnum"]=sentiments["neutralnum"]
    return data
