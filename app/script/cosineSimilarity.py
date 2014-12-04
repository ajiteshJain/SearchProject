import MySQLdb
import math
from nltk.corpus import stopwords
from collections import Counter
import operator
cachedStopWords = stopwords.words("english")

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
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
	counts = Counter(query.split())
	for word in counts:
		counts[word] = 1 + math.log(counts[word],10)	
	return counts

def GetSimilarityRanks(searchString):
	counts = GetQueryVector(searchString)
	#print counts
	query = "select URL,Word,Frequency,IDF from WordFrequency WHERE Word IN("+','.join('"'+i+'"' for i in counts)+")"
	print query
	if len(counts) == 0:
		return []
	numRows = cur.execute(query)
	wordChecked = []
	documentVectors = {}
	for i in range(numRows):
		row = cur.fetchone();
		if row[0] not in documentVectors:
			documentVectors[row[0]] = {}
		documentVectors[row[0]][row[1]] = 1 + math.log(row[2],10)
		if row[1] not in wordChecked:
			counts[row[1]] = counts[row[1]] * float(row[3])
			wordChecked.append(row[1])
	query = "select URL,Length from DocumentVectorLength"
	numRows = cur.execute(query)
	#print documentVectors
	dotProducts={}
	for i in range(numRows):
		dotProduct = 0.0
		row = cur.fetchone()
		if row[0] in documentVectors:
			for word in counts:
				if word in documentVectors[row[0]]:
					dotProduct += documentVectors[row[0]][word] * counts[word]
			dotProducts[row[0]] = dotProduct/row[1];
	sorted_x = sorted(dotProducts.items(), key=operator.itemgetter(1), reverse=True)
	#print sorted_x
	result = []
	for element in sorted_x:
		result.append(element[0])
	#print result
	return result

