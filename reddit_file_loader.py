#!/usr/bin/env python
# coding: utf-8

import csv
import sys
import json
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime as dt
from datetime import datetime
import praw
import itertools
import sqlalchemy
import time
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


# This script extracts data from the Reddit using the PRAW wrapper 
# from a list of Subreddits and appends them into a csv object

#Define Output Directory for csv Files

output_directory = "My/Path/"

#Datetime value that will be appended to csv file name

today = dt.datetime.now()

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
# and appends the data to a dict and dumps the csv file into our directory.

for i in subs:
    for submission in r.subreddit(i).new(limit=10):
        to_dict = vars(submission)
        sub_dict = {field:to_dict[field] for field in fields}
        list_of_items.append(sub_dict)
        output=DataFrame(list_of_items)
        output[['id','title', 'url','selftext','name', 'score', 'created_utc', 'num_comments','permalink']]= output[['id','title', 'url','selftext','name', 'score', 'created_utc', 'num_comments','permalink']].astype(str)

output.to_csv(str(output_directory)+'reddit_data'+str(today)+'.csv')




