import MySQLdb
import sys
from collections import Counter
import os
import traceback
import nltk
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
wnl = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))
db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                     user="root", # your username
                      db="cs6422") # name of the data base
db2 = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
                     user="root", # your username
                      db="cs6422") # name of the data base
cur2 = db2.cursor()
cur = db.cursor() 
cur.execute("SELECT url,filePath from pagedetails");
results = cur.fetchall()
count = 1

for row in results:
	try:
		url = row[0]
		filePath = row[1]
		if ".ps" in url:
			continue
			
		with open(filePath) as fileContent:
			wordCount = Counter()
			for line in fileContent:
				segmentedLine = re.findall("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",line)#line.rstrip().split()
				if len(segmentedLine) == 0:
					continue
				for word in segmentedLine:
					lowerWord = word.lower()
					if lowerWord in stopWords or not any(c.isalpha() for c in word):
						continue
					else:
						wordCount += Counter({wnl.lemmatize(lowerWord) : 1})

			query = 'INSERT INTO BetterWordFrequency(url,word,frequency) VALUES '
			for word,freq in wordCount.items():
				if any(c.isalpha() for c in word):
					query += "('"+MySQLdb.escape_string(url)+"','"+MySQLdb.escape_string(word)+"',"+str(freq)+"),"

			query = query[0:-1] + " ON DUPLICATE KEY UPDATE frequency = frequency + VALUES(frequency)"
			cur2.execute(query)
			db2.commit()	

	except:
		e = sys.exc_info()[0]
		print traceback.format_exc()
	finally:
		print "Done ",url, " Count = ",count
		count = count + 1
		#cur.close()
		#cur2.close()
cur.close()
cur2.close()
