SearchProject
=============

DB Impl Searching Project

How to run the project:

To run this project, you need to install the following:

1. python 2.7 
  -you need to install flask and MySQLdb libraries in python
2. MySQL
3. Contact Srishti for the data set (.sql file)
4. Run a Mysql server using : >>mysql.server start
5. On your mysql command line, import the .sql file.
6. You can now run the project by typing "python run.py" on the command line in the SearchProject folder.
7. That will provide a URL address like "127.0.0.1:5000". Go to this address in an HTML browser and search using the input box.

--------------------------------------------------------------------------------------------------------------------------

Directory structure:

GephiData folder contains the csv data files that were created using the Mysql database to be used as input for Gephi for grpah visualizations.

crawler folder contains the code used to crawl the cc.gatech.edu domain

app folder contains all the code related to data processing, connecting to the DB, searching, and display of returns on a browser.

run.py file runs the local server, so that the search engine can be used on a browser.

--------------------------------------------------------------------------------------------------------------------------




