from flask import render_template,request
from app import app
import json

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
	results = ['www.cc.gatech.edu','www.sify.com','www.google.com']#search(searchString)
	return json.dumps(results)

