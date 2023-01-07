import pandas as pd

import jellyfish
import nltk.corpus
from nltk.corpus import stopwords
import math
import re
from collections import Counter

WORD = re.compile(r"\w+")
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
def remove_token(text):
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    stop = stopwords.words('english')
    text = " ".join([word for word in text.split() if word not in (stop)])
    return text

def give_mathching_score(tags,text):
    text=remove_token(text)

    jaro_distance=jellyfish.jaro_distance(tags,text)
    vector1 = text_to_vector(tags)
    vector2 = text_to_vector(text)

    cosine = get_cosine(vector1, vector2)
    return (jaro_distance+cosine)/2

def get_relative_score(tags,video_data,captions):
    # if(int(video_data["viewCount"])!=0):
    # like_ratio=(int(video_data["likeCount"])/int(video_data["viewCount"]))*100
    # comment_ratio=(int(video_data["commentCount"])/int(video_data["viewCount"]))*100
    similarity_caption=give_mathching_score(tags,captions)
    similarity_title=give_mathching_score(tags,video_data['Title'])
    similarity_description=give_mathching_score(tags,video_data['Description'])
    final_similarity=(similarity_caption * (0.4))+(similarity_description * (0.35))+(similarity_title * (0.25))
    
    return 100*final_similarity

# 0.35 - Audio Text - 0.4
# 0.3 - Descp - 0.35
# 0.2 - Title - 0.25
# 0.15 - Image Text