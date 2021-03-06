#############################################################################################
# Create submissions Table                                                                      
# by Jack Hulbert                                                                         
# April 2020                                                                                
# https://github.com/jackhulbertpdx/GoingPlacesWithPraw                            
# ----------------------------------------------------------------------------------------- 
# Script that can be used to initiate a PostGres table to host the data acquired from Reddit in Ingestion.py
#     
#                                                                                           
#############################################################################################


#Initiates Postgre database table for reddit feed.


import psycopg2

conn = psycopg2.connect("dbname=db user=user password=pw port=5432")

cur = conn.cursor()


#Create Table

cur.execute("CREATE TABLE submissions (id varchar(200000),title varchar(100000),url varchar(200000),selftext varchar (1000000),name varchar(200000),created_utc varchar(200000),num_comments varchar(200000),permalink varchar(200000));")


# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
