#!/usr/bin/python3.4
import cherrypy
import mimetypes
import os
import configparser
import json
from jinja2 import Environment, FileSystemLoader
class Server():

	@cherrypy.expose
	def index(self):

		template = env.get_template('index.html')
		return template.render()

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
cherrypy.quickstart(Server(),'/',conf)
