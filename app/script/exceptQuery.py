import MySQLdb
from searching import *
from cosineSimilarity import *
import re

def GetExceptList():
	return ['except', 'but', 'without', 'excluding', 'omitting']


def exceptQueries(query):
	db = MySQLdb.connect(host="127.0.0.1",user="root", db = "cs6422" )
	cur = db.cursor()
	exceptList = GetExceptList()
	splitQuery = []
	for elem in exceptList:
		if elem in query:
			splitQuery = query.split(elem)
			break

	if len(splitQuery) == 0:
		return []
	keyword = splitQuery[0]
	removeWords = splitQuery[1].split()
	result = SearchKeywordForExcept(keyword)	
	newResults = result.copy()
	
	for url in result:
		if re.search( r'.*ps', url):
			del newResults[url]
			continue
		urlFreqOfRemoveWords  = []
		for word in removeWords:
			# if word in url:
			# 	print "deleting:", url
			# 	del newResults[url]
			# 	continue
			cur.execute("SELECT Frequency, TFIDF FROM WordFrequency WHERE Word='{0}' and URL='{1}'".format(word, url))
			if cur.rowcount != 0:
				row = cur.fetchone()
				urlFreqOfRemoveWords.append(row[0])
		
		if len(urlFreqOfRemoveWords)>0  and max(urlFreqOfRemoveWords) > 2:
			print urlFreqOfRemoveWords
			if url in newResults:
				print "deleting:", url
				del newResults[url]


	print len(result)
	print len(newResults)
	sortedResults = sorted(newResults.items(), key=lambda x: x[1], reverse=True)
	res = []
	for elem in sortedResults:
		res.append(elem[0])
	return res	


# res = exceptQueries("georgia tech faculty except chau")
# for elem in res[:10]:
# 	print elem

	
	
