

import psycopg2

conn = psycopg2.connect("dbname=db user=user password=pw port=5432")

cur = conn.cursor()




cur.execute("CREATE TABLE submissions (id varchar(200000),title varchar(100000),url varchar(200000),selftext varchar (1000000),name varchar(200000),created_utc varchar(200000),num_comments varchar(200000),permalink varchar(200000));")


# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()