import MySQLdb

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
			print type(row[0])
			if row[1] not in results:
				results[row[1]] = 0
			if (row[0] is None) or (len(row[0]) == 0):
				continue
			else:
				results[row[1]] += float(row[0])

	sortedResults = sorted(results.items(), key=lambda x: x[1], reverse=True)[:10]

	print sortedResults

	return sortedResults

