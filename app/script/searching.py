import MySQLdb
from nltk.corpus import stopwords

cachedStopWords = stopwords.words("english")

def SearchWord(word):
	db = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()

	cur.execute("SELECT TFIDF, URL from WordFrequency where Word = '{0}' ORDER BY TFIDF LIMIT 10".format(word))
	results = []
	for i in range(cur.rowcount):
		row = cur.fetchone()
		results.append(row[1])

	return results


def SearchMultipleWords(query):
	# summing tf--idf
	words = query.split()
	db = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word = '{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			# print type(row[0])
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (len(row[0]) == 0):
				continue
			else:
				results[row[1]] += float(row[0])

	sortedResults = sorted(results.items(), key=lambda x: x[1], reverse=True)
	res = []
	for elem in sortedResults:
		res.append(elem[0])
	print sortedResults

	return res

def SearchMultopleWordsRemovingStopWords(query):
	# summing tf idf after removing stop words from the query	
	query = ' '.join([word for word in query.split() if word not in cachedStopWords])
	results = SearchMultipleWords(query)
	return results

def SearchMultipleWordsWithAlexaPageRank(query):
	words = query.split()
	db = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word='{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (len(row[0] == 0):
				continue
			else:
				results[row[1]] += float(row[0])

	for elem in results:
		cur.execute("SELECT alexaPageRank from pagedetails where url='{0}'".format(elem))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			results[elem] * = int(row[0])

	return results

def SearchMultipleWordsWithGooglePageRank(query):
	words = query.split()
	db = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word='{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (len(row[0] == 0):
				continue
			else:
				results[row[1]] += float(row[0])

	for elem in results:
		cur.execute("SELECT googlePageRank from pagedetails where url='{0}'".format(elem))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			results[elem] * = int(row[0])

	return results

def consineSimWithWordFreq(query):
	# words = query.split()
	# db = MySQLdb.connect(user="root", db = "cs6422" )
	# cur = db.cursor()
	
	# results = {}
	# queryVector = {}

	# cur1 = db1.cursor()
	# cur1.execute("SELECT count(distinct URL) from WordFrequency")
	# row1 = cur1.fetchone()
	# TotalURL = int(row1[0])

	# for word in words:
	# 	if word not in queryVector:
	# 		queryVector[word] = 









