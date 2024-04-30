# kudos-service
A flask based microservice that allows users say "Kudos!" to cool features in my portfolio

## Overview
The kudos is a Flask based python application that fields request related to creating Kudos objects. A kudos is a representation of a user liking a feature on my personal website. This is organized by path and hashtag to be used with HTML links. Every time a user clicks on a Kudos item, the count of Kudos will be updated for that path. 

## Setup
You'll need to downlaod python, and then pip install the requirements.txt in a venv environment. Then you can run the application with "flask run". 
To run this application you'll need to provide a DB_CONNECTION_STRING url, and also have a properly configured database, database user, and tables. To help with migrations you can use Flask migration. 
