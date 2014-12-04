from flask import render_template,request
from app import app
import json
from app import app
from script.searching import *
from script.cosineSimilarity import *
from script.exceptQuery import *
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	user = {'nickname': 'Miguel', 'name':'MM'}  # fake user
	posts = [  # fake array of posts
	    { 
	        'author': {'nickname': 'John'}, 
	        'body': 'Beautiful day in Portland!' 
	    },
	    { 
	        'author': {'nickname': 'Susan'}, 
	        'body': 'The Avengers movie was so cool!' 
	    }
	]
	return render_template("searchEngine.html",
	                       title='Home',
	                       user=user,
	                       posts=posts)

@app.route('/search')
def search_main():
	searchString = request.args.get('searchString','')
	print "searchString", searchString

	words = searchString.split()
	exceptList = GetExceptList();
	for i in range(len(words)):
		if words[i] in exceptList:
			continue
		else:
			words[i] = wnl.lemmatize(words[i])
	searchString = ' '.join(words);
	print "searchString after lemmatization:",searchString			

	if " " not in searchString:
		results = SearchWord(searchString)
	else:
		res = exceptQueries(searchString)
		# print "here", res
		if len(res) != 0:
			results = res
		else:
			#results = GetSimilarityRanks(searchString)
			#results = SearchMultipleWordsWithAlexaPageRank(searchString)
			#results = SearchMultipleWordsWithGooglePageRank(searchString)
			results = SearchMultipleWords(searchString)


	# print results
	# results = ['www.cc.gatech.edu','www.sify.com','www.google.com']
	for i in range(len(results)):
		results[i] = unicode(results[i], errors='ignore')
	return json.dumps(results[:20])

