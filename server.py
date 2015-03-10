#! /usr/bin/env python3
import cherrypy
import os
import configparser
import json
from database import Database
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

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