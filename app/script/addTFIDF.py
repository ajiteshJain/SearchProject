import MySQLdb
import csv
import math

db = MySQLdb.connect(user="root", db = "cs6422" )
db1 = MySQLdb.connect(user="root", db = "cs6422" )
cur = db.cursor()
cur1 = db1.cursor()

cur1.execute("SELECT count(distinct URL) from WordFrequency")
row1 = cur1.fetchone()
TotalURL = int(row1[0])

cur.execute("SELECT Word, URL, Frequency, ID from WordFrequency")

for i in range(cur.rowcount):
	# if i==2:
	# 	break
	if i%100==0:
		print i

	row = cur.fetchone()
	word = row[0]
	url = row[1]
	freq = row[2]
	idValue = row[3]
	cur1.execute("SELECT max(Frequency), ID from WordFrequency where URL='{0}'".format(url))
	row1 = cur1.fetchone()
	maxfreq = row1[0]
	tf= 0.5 + (0.5*freq)/maxfreq
	# print "TF",tf
	# print word
	
	cur1.execute('SELECT count(*) from WordFrequency where Word="{0}"'.format(word))
	# print cur1.rowcount
	row1 = cur1.fetchone()

	# print TotalURL, row1[0]
	temp = (TotalURL+ 0.0)/row1[0]
	idf = math.log(temp,10)
	tfidf = tf/idf
	# print "IDF",idf, word, idValue
	cur1.execute("UPDATE WordFrequency SET TF =%s, IDF=%s, TFIDF=%s WHERE ID=%s", (tf, idf,tfidf, idValue))
	db1.commit()


	# ALTER TABLE WordFrequency Add TFIDF FLOAT after IDF

