import MySQLdb

def SearchWord(word):
	db = MySQLdb.connect(user="root", db = "cs6422" )
	cur = db.cursor()
	cur.execute("SELECT * from WordFrequency where Word LIKE '{0}'".format(word))
	row = cur.fetchone()
	print cur.rowcount
	return cur.rowcount

