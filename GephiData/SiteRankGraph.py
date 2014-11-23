#!/usr/bin/python

import MySQLdb
import csv
import re
import networkx as nx
import pickle

db = MySQLdb.connect(user="root", db = "cs6422" )
cur = db.cursor()
cur.execute("SELECT serialNum, url from linkstatus")

AllNodes = {}
SiteNodes = {}

for i in range(cur.rowcount):
	row = cur.fetchone()
	AllNodes[row[1]] = row[0]
	urlParts = row[1].split('/', 4)
	if len(urlParts) < 4:
		urlToAdd = ""
		for elem in urlParts:
			urlToAdd += elem +'/'
		urlToAdd = urlToAdd [:-1]
		if urlToAdd not in SiteNodes:
			SiteNodes[urlToAdd] = []
		SiteNodes[urlToAdd].append(row[1])
		# SiteNodes[row[1]] = urlToAdd
	else:
		if urlParts[3] == '':
			if row[1][:-1] not in SiteNodes:
				SiteNodes[row[1][:-1]] = []
			SiteNodes[row[1][:-1]].append(row[1])
			# SiteNodes[row[1]] = row[1][:-1]
		else:
			node = urlParts[0]+'/'+urlParts[1]+'/'+urlParts[2]+'/'+urlParts[3]
			if node not in SiteNodes:
				SiteNodes[node] = []
			SiteNodes[node].append(row[1])
			# SiteNodes[row[1]] = node

print "done"
cur.execute("SELECT url, parentUrl FROM linkstructure")
print SiteNodes
# print AllNodes
SiteLinks = {} #start key, end value
DG=nx.DiGraph()
for i in range(cur.rowcount):
	row = cur.fetchone()
	if row[0] not in AllNodes:
		continue
	if row[1] not in AllNodes:
		continue

	start = ""
	end = ""
	for link, linklist in SiteNodes.items():
		if row[1] in linklist:
			start = link
		if row[0] in linklist:
			end = link

	if start != "" and end != "":
		SiteLinks[start] = end
		DG.add_node(start)
		DG.add_node(end)
		DG.add_edge(start, end)

print "done2"
pr = nx.pagerank(DG)
print pr

with open('./pr.pickle','wb' ) as handle:
	pickle.dump(pr,handle)

with open('./AllNodes.pickle','wb' ) as handle:
	pickle.dump(AllNodes,handle)


with open('./SiteNodes.pickle','wb' ) as handle:
	pickle.dump(SiteNodes,handle)

with open('./SiteLinks.pickle','wb' ) as handle:
	pickle.dump(SiteLinks,handle)

with open('./Graph.pickle','wb' ) as handle:
	pickle.dump(DG,handle)












