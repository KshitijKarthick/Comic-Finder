#! /usr/bin/env python3
import cherrypy
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

    comic_url = ""
    database  = None

    def __init__(self, configuration):
        ''' Initialization the URL of the comic and transcript '''

        self.comic_url = configuration['comic_url']
        self.database = Database(configuration['database_uri'])

    @cherrypy.expose
    def index(self):
        ''' Render the index page '''

        template = env.get_template('index.html')
        return template.render()

    @cherrypy.expose
    def find_comic(self, string):
        ''' Return the url of the comic requested based on the i/p String '''

        matched_entries=[]
        iterable_list=self.database.find_data(string)
        for entry in iterable_list:
            id = int(entry['id'])
            matched_entries.append(id)
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

    def __init__(self, database_uri ):
        ''' Initialization the URL of the comic and transcript '''

        self.client = MongoClient(database_uri)
        self.db = self.client.get_default_database()
        self.collection = self.db.xkcd

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
        link_id=0
        while(True):
            link_id+=1
            print(link_id)
            opener=urllib.request.build_opener()
            try:
                webpage=opener.open("http://www.xkcd.com/"+str(link_id)+"/info.0.json")
            except:
                if link_id == 404:
                    continue;
                else:
                    break;
            if webpage.status == 200:
                try:
                    comic_data = json.loads((webpage.readall()).decode("utf-8"))
                    self.insert_data({
                        'id':link_id,
                        'transcript': comic_data['transcript'],
                        'title': comic_data['title'],
                        'img': comic_data['img']
                    })
                except:
                    errors.append(link)
        print(errors," -> Could not be Downloaded does not follow the standard format")
        return errors

if __name__ == '__main__':
    ''' Setting up the Server with Specified Configuration'''

    server_config = configparser.RawConfigParser()
    env = Environment(loader=FileSystemLoader(''))
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
    server_port=server_config.get('Server','port')
    server_host=server_config.get('Server','host')
    comic_url=server_config.get('xkcd','url')
    database_uri=server_config.get('Database', 'database_uri')
    configuration = {
        'comic_url'     :   comic_url,
        'database_uri'  :   database_uri
    }
    cherrypy.config.update({'server.socket_host': server_host})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', server_port))})
    cherrypy.quickstart(Server(configuration),'/',conf)