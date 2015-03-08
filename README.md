# Comic Finder
Find XKCD Comics by searching for the String present in any of the comics, and the application lists the comics with the string.

## Functionality :
  * Crawl through all XKCD Comics
  * Search through the Transcripts of the Comics to find the specified string in any of the XKCD Comics

## Program Details :
  * Server runs on python3 using CherryPy as the web framework.
  * Clientside uses JQuery, Javascript, CSS, HTML.

## Working :
  * Client sends a GET request with the string, server responds back with the comic URL.

## Execution :
'''
# Install MongoDB
# Set up the Server and the Database with the xkcd info
    > cd Comic-Finder
    > sudo pip install -r requirements.txt
    > mongorestore xkcd
    > python server.py
# Open the Browser at localhost:5000
'''

## To Do :
  * Database Implementation.
  * Crawling through the Transcripts of the Comics.
  * AJAX Implementation.
  * UI/UX Design on Clientside.
