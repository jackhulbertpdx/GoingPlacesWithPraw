#############################################################################################
# Ingestion                                                                       
# by Jack Hulbert                                                                         
# April 2020                                                                                
# https://github.com/jackhulbertpdx/GoingPlacesWithPraw                            
# ----------------------------------------------------------------------------------------- 
# Ingests data from the Reddit PRAW Wrapper from user-defined subreddit feeds, filters, and
# loads data into a PostGreSQL table defined in Create Database.py
# In order to use this script you must first acquire your user credentials and create an app 
# using a Reddit developer account.
#############################################################################################



import csv
import io
from io import StringIO
import psycopg2
import glob
import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime as dt
from datetime import datetime
import praw
import sys
from dateutil import tz
import time


# This script extracts data from the Reddit using the PRAW wrapper 
# from a list of Subreddits and appends them into a csv object and loads into a PostgreSQL table



def get_reddit_data():
  
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
  #Write Output File to directory 
  data.to_csv(str(output_directory)+'reddit_data'+str(today)+'.csv', index = False, doublequote=True)


  ####################################################


  # Initiate PostGreSQL 
  conn = psycopg2.connect("dbname=db user=user password=pw port=port")
  cur = conn.cursor()

  # Grab most recent file written to copy into PG table
  list_of_files = glob.glob('directory/*') 
  latest_file = max(list_of_files, key=os.path.getctime)
  print(latest_file)
  with open(latest_file) as f:
      cur.copy_expert('COPY submissions(id, title,url,selftext,name,created_utc,num_comments,permalink) FROM STDIN WITH HEADER CSV', f)


  # Make the changes to the database persistent
  conn.commit()
  cur.close()
  conn.close()
  
get_reddit_data()
