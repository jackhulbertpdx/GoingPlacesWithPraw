#!/usr/bin/env python
# coding: utf-8

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

import sys
import json
import os
import glob
import pandas as pd
import numpy as np
from pandas import DataFrame
import texthero as hero
from texthero import preprocessing
import datetime as dt
from datetime import datetime
from dateutil import tz
import itertools
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re 
import urllib
from urllib.parse import urlparse


# This script extracts data from the Reddit using the PRAW wrapper 
# from a list of Subreddits and appends them into a csv object

#Define Output Directory for csv Files

output_directory = "/Users/Mydirectory/"

#Datetime value that will be appended to csv file name

today = dt.datetime.now()

#Create container for PRAW data and intercept fields from the Subreddit class

list_of_items = []
fields = ('id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink')

#Define list of Subreddits to query using PRAW

subs = ['Toyota','ToyotaTundra','ToyotaTacoma','Prius','4Runner','ToyotaHighlander','ToyotaSupra','cars','ToyotaPickup','JDM']

#Authenticate PRAW with Client Secret, User Agent, and ID

r = praw.Reddit(client_id='id',
                client_secret='secret',
                user_agent='agent')

# Function that initiates a call to each subreddit in the defined list 
# and appends the data to a dict and dumps the csv file into our directory.
for i in subs:
    for submission in r.subreddit(i).new(limit=None):
        to_dict = vars(submission)
        sub_dict = {field:to_dict[field] for field in fields}
        list_of_items.append(sub_dict)
        data=DataFrame(list_of_items)
        data[['id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink']]= data[['id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink']].astype(str)
#Convert UTC to Datetime
data['created_utc']=(pd.to_datetime(data['created_utc'],unit='s'))
#Write Output File
data.to_csv(str(output_directory)+'reddit_data'+str(today)+'.csv', index = False, doublequote=True)


####################################################

import csv
import io
from io import StringIO
import psycopg2
# Initiate PostGreSQL 
conn = psycopg2.connect("dbname=db user=user password=pw port=port")
cur = conn.cursor()
import glob
import os

list_of_files = glob.glob('directory/*') # * grab latest csv writtent to load into postgresql
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
with open(latest_file) as f:
    cur.copy_expert('COPY submissions(id, title,url,selftext,name,created_utc,num_comments,permalink) FROM STDIN WITH HEADER CSV', f)


# Make the changes to the database persistent
conn.commit()
cur.close()
conn.close()

