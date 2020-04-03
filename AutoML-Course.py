# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 13:48:44 2020

@author: ramon
"""

import praw
import pandas as pd

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

reddit = praw.Reddit(client_id='zUpDVFSKIvc4eA',
                     client_secret='a_kCROkKRCAEMhow7X16VOptpj8',
                     password='Novena1.',
                     user_agent='testscript by /u/rrg890',
                     username='rrg890')

subreddit = reddit.subreddit('coronavirus')

data = {"title":[] , "score":[]}
text = ""

for submission in subreddit.new(limit=1000):
    if text: 
        text = text + ".\n" + submission.title.replace(',','')
        
    else:
        text = submission.title.replace(',','')

client = language.LanguageServiceClient()

doc = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

sentences = client.analyze_sentiment(document=doc).sentences

for sentence in sentences:
    data["title"].append(sentence.text.content)
    data["score"].append(round(sentence.sentiment.score+1))

to_store = pd.DataFrame(data)

to_store.to_csv('data/data.csv', index=False)
to_store.to_string()