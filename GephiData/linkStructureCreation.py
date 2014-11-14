#!/usr/bin/python

import MySQLdb
import csv

# db = MySQLdb.connect(user="root", db = "/Users/sristhi/Documents/Fall14/DBImpl/SearchProject/GephiData/cs6422.sql" )
db = MySQLdb.connect(user="root", db = "cs6422" )
db1 = MySQLdb.connect(user="root", db = "cs6422" )

cur = db.cursor()
cur1 = db1.cursor()

cur.execute("SELECT url, parentUrl FROM linkstructure")

with open('linkStructure.csv', 'wb') as linkFile:
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

		cur1.execute("SELECT serialNum from linkstatus where url='{0}'".format(row[0]))
		if cur1.rowcount > 1:
			print "CHILDbug"
			print cur1.rowcount
			break

		if cur1.rowcount ==1:
			row1 = cur1.fetchone()
			# print row1
			child = row1[0]
			# print par, child
			csv_writer.writerow((par, child))

print "done"
	
	





