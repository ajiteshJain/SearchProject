import MySQLdb
from searching import *

def exceptQueries(query):
	exceptList = ['except', 'but', 'without', 'excluding', 'omitting']
	splitQuery = []
	for elem in exceptList:
		if elem in query:
			splitQuery = query.split(elem)
			break

	if len(splitQuery) == 0:
		return ""
	splitQuery

