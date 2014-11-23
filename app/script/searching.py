import MySQLdb
from nltk.corpus import stopwords
import collections

cachedStopWords = stopwords.words("english")

def SortResults(results):
	sortedResults = sorted(results.items(), key=lambda x: x[1], reverse=True)
	res = []
	for elem in sortedResults:
		res.append(elem[0])
	print res
	return res


def SearchWord(word):

	db = MySQLdb.connect(host="127.0.0.1",user="root", db = "cs6422" )
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
	db = MySQLdb.connect(host="127.0.0.1",user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word = '{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (row[0] == 0):
				continue
			else:
				results[row[1]] += row[0]

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
	db = MySQLdb.connect(host="127.0.0.1",user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word='{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (row[0] == 0):
				continue
			else:
				results[row[1]] += row[0]

	for elem in results:
		cur.execute("SELECT alexaPageRank from pagedetails where url='{0}'".format(elem))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			results[elem] *= float(row[0])

	return SortResults(results)

def SearchMultipleWordsWithGooglePageRank(query):
	words = query.split()
	db = MySQLdb.connect(host="127.0.0.1",user="root", db = "cs6422" )
	cur = db.cursor()
	results = {}
	for word in words:
		cur.execute("SELECT TFIDF, URL from WordFrequency where Word='{0}'".format(word))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (row[0] == 0):
				continue
			else:
				results[row[1]] += row[0]

	for elem in results:
		cur.execute("SELECT googlePageRank from pagedetails where url='{0}'".format(elem))
		for i in range(cur.rowcount):
			row = cur.fetchone()
			results[elem] *= int(row[0])

	return SortResults(results)


def consineSimWithWordFreq(test):

	db = MySQLdb.connect(user="root", db = "cs6422" )
	db1 = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()
	cur1 = db.cursor()
	cur.execute("SELECT count(distinct URL) from WordFrequency")
	row = cur.fetchone()
	N = int(row[0])

	wordFreq = collections.Counter(test.split()).most_common()
	wordFreq = sorted(wordFreq,key=collections.itemgetter(1), reverse = True)
	tfWT = {}
	idf = {}
	wt = {}
	norm = 0
	results = {}
	for elem in wordFreq:
		tfWT[elem[0]] = 1 + math.log(elem[1])
		cur1.execute("SELECT count(distinct URL) from WordFrequency where Word = '{0}'".format(elem[0]))
		row1 = cur1.fetchone()
		idf[elem[0]] = math.log(N/row1[0])
		wt[elem[0]] = tfWT[elem[0]] * idf[elem[0]]
		norm += math.pow(wt[elem[0]],2)

	norm = math.sqrt(norm)

	for elem in wt:
		wt[elem] = wt[elem]/norm

	# wt has the vector for the query now

	URLs = {}

	cur.execute("SELECT distinct url from WordFrequency")
	for i in range(cur.rowcount):
		URLs.append(row[0])
	for url in URLs:
		norm = 0
		tf = {}
		for word in wt:
			cur1.execute("SELECT Frequency from WordFrequency where URL=%s and Word= %s ", (url, word))
			row1 = cur1.fetchone()
			tf[word] = 1 + math.log(row1[0])
			norm += math.pow(tf[word],2)

		norm = math.sqrt(norm)
		res = 0
		for word in wt: 
			tf[word] /= norm
			res += tf[word]*wt[elem]
		results[url] = res

	resultsSorted = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
	return resultsSorted[:10]





