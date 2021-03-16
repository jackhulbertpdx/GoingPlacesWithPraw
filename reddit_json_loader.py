#!/usr/bin/env python
# coding: utf-8


import sys
import json
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime as dt
from datetime import datetime
import praw
import urllib.request
import itertools


# This script extracts data from the Reddit using the PRAW wrapper 
# from a list of Subreddits and appends them into a JSON object

#Define Output Directory for JSON Files

output_directory = "/Home/Name/Path/"

#Datetime value that will be appended to JSON file name

now = dt.datetime.now()

#Create container for PRAW data and intercept fields from the Subreddit class

list_of_items = []
fields = ('id','title', 'url','selftext','name', 'score', 'created_utc', 'num_comments','permalink')

#Define list of Subreddits to query using PRAW

subs = ['Toyota','ToyotaTundra','ToyotaTacoma','Prius','4Runner','ToyotaHighlander','ToyotaSupra','cars','ToyotaPickup']

#Authenticate PRAW with Client Secret, User Agent, and ID

r = praw.Reddit(client_id='id',
                client_secret='secret',
                user_agent='agent')

# Function that initiates a call to each subreddit in the defined list 
# and appends the data to a dict and dumps the JSON file into our directory.

for i in subs:
    for submission in r.subreddit(i).new(limit=None):
        to_dict = vars(submission)
        sub_dict = {field:to_dict[field] for field in fields}
        list_of_items.append(sub_dict)

        json_str = json.dumps(list_of_items)

        
with open(str(output_directory)+'reddit_data'+str(today)+'.json', 'w') as f:
    json.dump(list_of_items, f)



