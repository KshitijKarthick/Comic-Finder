#!/usr/bin/python3.4
import cherrypy
import mimetypes
import os
import configparser
import json
import re
import pymongo
import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import Regex
from jinja2 import Environment, FileSystemLoader
from random import randint
class Server():
    '''
        Server Configuration:
        comic_url -> Base URL specified in server.conf
        transcript_url -> Transcipt URL specified in server.conf
    '''

    transcript_url = ""
    comic_url = ""
    database = ""

    def __init__(self, configuration):
        ''' Initialization the URL of the comic and transcript '''

        self.transcript_url = configuration['transcript_url']
        self.comic_url = configuration['comic_url']
        self.database = Database(configuration['database_url'], configuration['database_port'])

    @cherrypy.expose
    def index(self):
        ''' Render the index page '''

        template = env.get_template('index.html')
        return template.render()

    @cherrypy.expose
    def find_comic(self, string):
        ''' Return the url of the comic requested based on the i/p String '''

        # Temporary Random Url Generated for Debuggin Purpose
        # return json.dumps({string:[comic_url + str(randint(1,100))]})
        matched_entries=[]
        iterable_list=self.database.find_data(string)
        for entry in iterable_list:
            matched_entries.append(int(entry['id']))
        return json.dumps({string:matched_entries})

class Database():
    '''
        Database Configuration:
        client -> MongoDb client.
        db -> Retrieve the Database.
        collection -> Retrieve the Collection.
    '''

    client = ""
    db = ""
    collection = ""

    def __init__(self, database_url, database_port ):
        ''' Initialization the URL of the comic and transcript '''

        self.client = MongoClient(database_url, database_port)
        self.db = self.client.comics
        self.collection = self.db.comics

    def insert_data(self, data):
        ''' Insert the data into the Collection '''

        self.collection.insert(data)

    def find_data(self, string):
        ''' Find the string in the Database '''

        pattern = re.compile(string, re.IGNORECASE)
        regex = Regex.from_native(pattern)
        regex.flags ^= re.UNICODE
        return self.collection.find({"transcript":regex})

    def get_data(self):
        ''' Obtain the data for storing into the Collection '''
        errors=[]
        link_id=1
        while(1):
            print(link_id)
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-agent','Mozilla/5.0')]
            webpage=opener.open("http://www.explainxkcd.com/wiki/index.php/"+str(link_id))
            if webpage.status == 200:
                html = webpage.readall()
                soup = BeautifulSoup(html)
                transcript = soup.find('dl')
                if transcript != None:
                    self.insert_data({'id':link_id,'transcript':transcript.get_text()})
                else:
                    errors.append(link_id)
            elif link_id == 404:
                continue;
            else:
                break
            link_id+=1
        print(errors)
        print(" -> Could not be Downloaded does not follow the standard format")

if __name__ == '__main__':
    ''' Setting up the Server with Specified Configuration'''

    server_config = configparser.RawConfigParser()
    env = Environment(loader=FileSystemLoader(''))
    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
    conf = {
        '/':{
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './resources'
        }
    }
    server_config.read('server.conf')
    transcript_url=server_config.get('URL','transcript_url')
    comic_url=server_config.get('URL','comic_url')
    database_url=server_config.get('Database', 'database_url')
    database_port=server_config.get('Database', 'database_port')
    configuration = {
        'transcript_url' : transcript_url,
        'comic_url' : comic_url,
        'database_url' : database_url,
        'database_port' : int(database_port)
    }
cherrypy.quickstart(Server(configuration),'/',conf)
