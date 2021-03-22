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

output_directory = "/Users/jackhulbert/Desktop/Data Science Projects/Reddit Project/Raw Data/"

#Datetime value that will be appended to csv file name

today = dt.datetime.now()

#Create container for PRAW data and intercept fields from the Subreddit class

list_of_items = []
fields = ('id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink')

#Define list of Subreddits to query using PRAW

subs = ['Toyota','ToyotaTundra','ToyotaTacoma','Prius','4Runner','ToyotaHighlander','ToyotaSupra','cars','ToyotaPickup','JDM']

#Authenticate PRAW with Client Secret, User Agent, and ID

r = praw.Reddit(client_id='GKhbQBE_zmIfSA',
                client_secret='ak9O7S3dSduQ4FPCZ1GpacdcTRo0VQ',
                user_agent='Secret-Strain-8422')

# Function that initiates a call to each subreddit in the defined list 
# and appends the data to a dict and dumps the csv file into our directory.
for i in subs:
    for submission in r.subreddit(i).new(limit=None):
        to_dict = vars(submission)
        sub_dict = {field:to_dict[field] for field in fields}
        list_of_items.append(sub_dict)
        data=DataFrame(list_of_items)
        data[['id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink']]= data[['id','title', 'url','selftext','name', 'created_utc', 'num_comments','permalink']].astype(str)
data['created_utc']=(pd.to_datetime(data['created_utc'],unit='s'))
data.to_csv(str(output_directory)+'reddit_data'+str(today)+'.csv', index = False, doublequote=True)


####################################################

import csv
import io
from io import StringIO
import psycopg2
conn = psycopg2.connect("dbname=reddit user=postgres password=jh12345 port=5432")
cur = conn.cursor()
import glob
import os

list_of_files = glob.glob('/Users/jackhulbert/Desktop/Data Science Projects/Reddit Project/Raw Data/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
with open(latest_file) as f:
    cur.copy_expert('COPY submissions(id, title,url,selftext,name,created_utc,num_comments,permalink) FROM STDIN WITH HEADER CSV', f)


#cur.execute("""INSERT INTO submissions (id,title, url,selftext,namepip, created_utc, num_comments,permalink) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s);""" ,  (str(output['id']), str(output['title']), str(output['url']),str(output['selftext']),str(output['name']),str(output['score']),str(output['created_utc']),str(output['num_comments']),str(output['permalink'])))
# Make the changes to the database persistent
conn.commit()
cur.close()
conn.close()

