# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 07:21:05 2016

@author: gus
"""

import twitter
import pandas as pd
import requests
import json
from constants import *

    
def call_watson(mydf):
    stuff = mydf.to_string()
    clean_text = ''.join([i if ord(i) < 128 else ' ' for i in stuff])
    response = requests.post(WATSON_URL + "/v2/profile",
                          auth=(WATSON_USERNAME, WATSON_PASSWORD),
                          headers = {"content-type": "text/plain"},
                          data=clean_text
                          )
    out = json.loads(response.text)
    return out
    
def parse_response(out):
    myData = []
    for row in out['tree']['children']:
        for value in row['children']:
            for thing in value['children']:
                myRow = {}
                myRow['category'] = value['category']
                myRow['percentage'] = value['percentage']
                myRow['name'] = thing['name']
                myRow['percentile'] = thing['percentage']
                myRow['sampling_error'] = thing['sampling_error']
                myData.append(myRow)
    watson_df = pd.DataFrame(myData)
    ord_df = watson_df[['category', 'percentage', 'name', 'percentile', 'sampling_error']]
    return ord_df
        
        
def get_tweets(username):
    api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                      consumer_secret=TWITTER_CONSUMER_SECRET,
                      access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                      access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
    
    statuses = api.GetUserTimeline(screen_name=username, count=200)
    return statuses

def format_tweets(statuses):       
    mytweets = {'Tweets': [x.text for x in statuses]}
    df = pd.DataFrame(mytweets)
    flat = df.set_index('Tweets')
    return flat
 


       
    
    
