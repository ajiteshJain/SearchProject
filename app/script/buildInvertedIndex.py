import MySQLdb
from collections import Counter
import os
import nltk
import re
from nltk.stem.snowball import SnowballStemmer


db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="echinodermata", # your password
                      db="cs6422") # name of the data base
cur = db.cursor() 
stemmer = SnowballStemmer("english")
try:
	for root, dirs, files in os.walk("../data/data"):
		for file1 in files:
			with open(os.path.join(root, file1), 'r') as f:
				content = re.split("[^\w'-]+",f.read().replace('\n',' '))
				c = Counter(content)
				URL = f.name.replace('!','/')[13:]
				for elem in c:
					rootWord = stemmer.stem(elem)
					numRows = cur.execute("SELECT * from WordFrequency WHERE URL=%s AND Word=%s", (URL, rootWord));
					# if (url,rootWord) not in table add it along with frequency
					if numRows == 0:
						cur.execute("INSERT into WordFrequency(Word, URL, Frequency) values (%s,%s,%s)", (rootWord, URL, c[elem]))
					# else add to the frequency
					else:
						freq = cur.fetchone()[2]
						cur.execute("UPDATE WordFrequency SET Frequency=%s WHERE URL=%s AND Word=%s", (c[elem]+freq, URL, rootWord))
					db.commit()
except:
	print "Exception!!::"
finally:
	cur.close()
