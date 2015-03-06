#!/usr/bin/python3.4
import cherrypy
import mimetypes
import os
import configparser
import json
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

    def __init__(self, transcript_url, comic_url):
        ''' Initialization the URL of the comic and transcript '''

        Server.transcript_url = transcript_url
        Server.comic_url = comic_url

    @cherrypy.expose
    def index(self):
        ''' Render the index page '''

        template = env.get_template('index.html')
        return template.render()

    @cherrypy.expose
    def find_comic(self, string):
        ''' Return the url of the comic requested based on the i/p String '''

        # Temporary Random Url Generated for Debuggin Purpose
        return json.dumps({string:[comic_url + str(randint(1,100))]})

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
cherrypy.quickstart(Server(transcript_url, comic_url),'/',conf)
