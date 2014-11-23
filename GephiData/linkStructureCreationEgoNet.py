#!/usr/bin/python

import MySQLdb
import csv

# db = MySQLdb.connect(user="root", db = "/Users/sristhi/Documents/Fall14/DBImpl/SearchProject/GephiData/cs6422.sql" )
db = MySQLdb.connect(user="root", db = "cs6422")
db1 = MySQLdb.connect(user="root", db = "cs6422")

cur = db.cursor()
cur1 = db1.cursor()
urlList = {}

cur.execute("SELECT url FROM linkstructure where parentUrl='{0}'".format("http://www.cc.gatech.edu"))
print cur.rowcount

cur1.execute("SELECT serialNum FROM linkstatus WHERE url='{0}'".format("http://www.cc.gatech.edu"))
print cur1.rowcount
row1  = cur1.fetchone()
PARENTNODE = row1[0]
urlList[row1[0]] = "http://www.cc.gatech.edu"
with open('newData/linkStructureEgonet.csv', 'wb') as linkFile:
	csv_writer = csv.writer(linkFile)
	for i in range(cur.rowcount):
		# if i==2:
		# 	break;
		row = cur.fetchone()

		cur1.execute("SELECT serialNum from linkstatus where url='{0}'".format(row[0]))
		if cur1.rowcount > 1:
			print "CHILDbug"
			print cur1.rowcount
			break

		if cur1.rowcount ==1:
			row1 = cur1.fetchone()
			# print row1
			child = row1[0]
			urlList[row1[0]] = row[0]
			csv_writer.writerow((PARENTNODE, child))

print "done"

with open("newData/nodesEgoNet.csv", 'wb') as nodeFile:
	csv_writer = csv.writer(nodeFile)
	for elem in urlList: 		
		csv_writer.writerow((elem, urlList[elem]))




	
	





