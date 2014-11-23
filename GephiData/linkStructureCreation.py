#!/usr/bin/python

import MySQLdb
import csv

# db = MySQLdb.connect(user="root", db = "/Users/sristhi/Documents/Fall14/DBImpl/SearchProject/GephiData/cs6422.sql" )
db = MySQLdb.connect(user="root", db = "cs6422",passwd = 'echinodermata' )
db1 = MySQLdb.connect(user="root", db = "cs6422" ,passwd= 'echinodermata')

cur = db.cursor()
cur1 = db1.cursor()
urlList = []

cur.execute("SELECT url, parentUrl FROM linkstructure where parentUrl='{0}'".format("http://www.cc.gatech.edu"))
print cur.rowcount
with open('newData/linkStructureEgonet.csv', 'wb') as linkFile:
	csv_writer = csv.writer(linkFile)
	for i in range(cur.rowcount):
		if i%10000==0:
			print i
		# if i==2:
		# 	break;
		row = cur.fetchone()
		cur1.execute("SELECT serialNum from linkstatus where url='{0}'".format(row[1]))
		
		if cur1.rowcount > 1:
			print "PARbug"
			print cur1.rowcount
			break

		row1 = cur1.fetchone()
		par = row1[0]
		urlList.append(par)
		cur1.execute("SELECT serialNum from linkstatus where url='{0}'".format(row[0]))
		if cur1.rowcount > 1:
			print "CHILDbug"
			print cur1.rowcount
			break

		if cur1.rowcount ==1:
			row1 = cur1.fetchone()
			# print row1
			child = row1[0]
			urlList.append(child)
			# print par, child
			csv_writer.writerow((par, child))

print "done"
urlList = list(set(urlList))
with open("newData/nodesEgoNet.csv", 'wb') as nodeFile:
	csv_writer = csv.writer(nodeFile)
	for elem in urlList: 
		cur.execute("select serialNum from linkstatus where url='{0}'".format(elem))
		if cur.rowcount == 1:		
			row = cur.fetchone()
			csv_writer.writerow((row[0], elem))
		else:
			print "node missing"



	
	





