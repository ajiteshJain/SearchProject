import MySQLdb
import math

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="echinodermata", # your password
                      db="cs6422") # name of the data base
cur = db.cursor()
cur.execute("SELECT DISTINCT(URL) FROM WordFrequency")
rows = cur.fetchall()
documents = []
for row in rows:
	documents.append(row[0])

for document in documents:
	vectorLength = 0;
	numRows = cur.execute("SELECT Frequency FROM WordFrequency WHERE URL='{0}'".format(document))
	for i in range(numRows):
		row = cur.fetchone()
		normalizedFrequency = 1 + math.log(row[0],10)
		vectorLength = vectorLength + normalizedFrequency * normalizedFrequency
	vectorLength = math.sqrt(vectorLength)
	cur.execute("INSERT into DocumentVectorLength(URL,Length) VALUES(%s,%s)",(document,vectorLength))
	db.commit()
