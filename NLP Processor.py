# coding: utf-8

import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
import os
import glob
import texthero as hero
from texthero import preprocessing
import datetime as dt
from datetime import datetime
from dateutil import tz
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re 
import pandas.io.sql as sqlio
import csv
import io
from io import StringIO
import psycopg2
conn = psycopg2.connect("dbname=reddit user=postgres password=jh12345 port=5432")
cur = conn.cursor()
import glob


#Today
today = dt.datetime.now()



#Load Data from PostgreSQL Table
sql= "SELECT * from submissions"
data = sqlio.read_sql_query(sql, conn)
conn = None
print(data)

#Write Directory
output_directory = "/Users/jackhulbert/Desktop/Data Science Projects/Reddit Project/Processed Data/"

# Make the changes to the database persistent
cur.close()


########################################################

#Data Conversion

data['body']= data['selftext']    


#Function to clean text columns, removing whitespace, punctuations, and stopwords
clean_text = [preprocessing.fillna,
                   preprocessing.lowercase,
                   preprocessing.remove_punctuation,
                   preprocessing.remove_whitespace,
                   preprocessing.remove_diacritics,
                   preprocessing.remove_brackets,
                   preprocessing.remove_stopwords
                  ]

#Define new columns for cleaned text 
data['clean_title'] = hero.clean(data['title'], clean_text)
data['clean_body'] = hero.clean(data['body'], clean_text)
#Apply cleaning functions to text columns
for n in data['clean_title'],data['clean_body']:
    [n.replace('{','')]
    [n.replace('}','')]
    [n.replace('(','')]
    [n.replace(')','')]



#One of the outcomes of this exercise is to give the end user the ability to search for permutations of owners mentioning the make and model of their car.
#Create a list from a range of years to scan text for customers mentioning vintage of their Toyota

years = "|".join(map(str,(range(1940,2022))))

#Extract year values from text columns

data['body_year'] = data['body'].str.extract(f'({years})')
data['title_year'] = data['title'].str.extract(f'({years})') 
data['Model Year']=data['body_year'].fillna(data['title_year'])


#Apply sentiment algorithim to 'Body' field where the user typically enters their message or post.

text = data['body'].astype(str) #Column being evaluated from dataframe
scores = [] #Container that will house the numerical score given by SID
sid = SentimentIntensityAnalyzer() #Define Sentiment Model 

#Map sentiment scores to objects in Dataframe, scores will range from -1 to 1
for word in text:
    ss = sid.polarity_scores(word)
    scores.append(ss['compound'])
data['Sentiment'] = scores

#Create dimensional buckets for sentiment scores for easier use
data['Sentiment_Label']= np.where(data['Sentiment']>.15,'Positive',
                            np.where(data['Sentiment']>=-.15,'Neutral','Negative'))

#Drop unwanted cols from processing
data.drop(['title_year','body_year','selftext'], axis=1)

#//STEP 2//#
#Read in CSV defined and managed by user
classification = pd.read_csv('/Users/jackhulbert/Desktop/Data Science Projects/Reddit Project/Classification.csv')

#Pivot data to make each column a keyword class and cell values the keywords from each class
keywords = DataFrame(classification).pivot( columns ='Category',values='Keywords')

#Convert each class in taxonomy to a list and remove NaN values
context = [x for x in keywords['Context'].tolist() if str(x) != 'nan']
model = [x for x in keywords['Model'].tolist() if str(x) != 'nan']
subject= [x for x in keywords['Subject'].tolist() if str(x) != 'nan']

#Combine Text columns 'Body' and 'Title ' into one text object so that only one column needs to be scanned using the above lists
data['combination']= (data['clean_body'].str.cat(data['clean_title'],sep=" "))

#Extract keywords values from each list and return match into new column
data['context'] = data['combination'].str.extract('(' + '|'.join(context) + ')')
data['subject'] = data['combination'].str.extract('(' + '|'.join(subject) + ')')
data['model'] = data['combination'].str.extract('(' + '|'.join(model) + ')')

#Drop unwanted cols from processing
data=data.drop(['combination','combination'], axis=1)
data['write_date'] = today

#Write
data.to_csv(str(output_directory)+'reddit_data'+str(today)+'.csv', index = False, doublequote=True)
