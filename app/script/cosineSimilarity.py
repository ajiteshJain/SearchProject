import MySQLdb
import math
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="echinodermata", # your password
                      db="cs6422") # name of the data base
cur = db.cursor()

def GetAllDocuments():
	cur.execute("SELECT URL FROM DocumentVectorLength")
	rows = cur.fetchall()
	documents = []
	for row in rows:
	        documents.append(row[0])
	return documents

def GetQueryVector(searchString):
	#remove stop words
	query = ' '.join([word for word in searchString.split() if word not in cachedStopWords])
	


def GetSimilarityRanks(searchString):
	documents = GetAllDocuments();
	for document in 

