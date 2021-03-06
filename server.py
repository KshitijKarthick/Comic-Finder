#! /usr/bin/env python3
import cherrypy
import os
import configparser
import json
from database import Database
from jinja2 import Environment, FileSystemLoader


class Server():
    '''
        Server Configuration:
        comic_url -> Base URL specified in server.conf
        transcript_url -> Transcipt URL specified in server.conf
    '''

    comic_url = ""
    database = None

    def __init__(self, configuration):
        """ Initialization the URL of the comic and transcript """

        self.comic_url = configuration['comic_url']
        self.database = Database(configuration['database_uri'])

    @cherrypy.expose
    def index(self):
        """ Render the index page """

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        template = env.get_template('index.html')
        return template.render()

    @cherrypy.expose
    def bulk_get_comic_details(self, list_of_comics):
        """ Returns the Comic Details of list of comics (max 10) """

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        data = []
        list_of_comics = json.loads(list_of_comics)
        limit = len(list_of_comics) if len(list_of_comics) <= 10 else 10
        for id in range(limit):
            data.append(json.loads(self.get_comic_details(list_of_comics[id])))
        return json.dumps(data)

    @cherrypy.expose
    def no_of_comics(self):
        """ Return the count of no of comics """

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        return json.dumps({
            "count": self.database.get_count()
        })

    @cherrypy.expose
    def get_comic_details(self, comic_id):
        """ Get Comic details for specified comic id """

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        comic_details = self.database.get_comic(comic_id)
        if comic_details is None:
            comic_details = {}
        else:
            del comic_details["_id"]
        return json.dumps(comic_details)

    @cherrypy.expose
    def find_comic(self):
        ''' Return comic details requested based on the i/p String '
            Return Type JSON object Json[List[Dictionary]]
            Keys of Dictionary:
                id          -> Comic Id
                img         -> Comic image
                title       -> Comic title
                transcript  -> Comic transcript
        '''

        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        try:
            received_data = cherrypy.request.body.read()
            decoded_data = json.loads(received_data.decode())
            string = decoded_data['string']
            limit = decoded_data['limit']
            phrase = decoded_data['phrase']
            skip = decoded_data['skip']
        except KeyError:
            raise cherrypy.HTTPError(500)
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        matched_entries = []
        iterable_list = self.database.search_data(
            string, phrase, limit, skip
        )
        for entry in iterable_list:
            id = int(entry['id'])
            self.database.increment_rank(id)
            matched_entries.append({
                "id": int(entry['id']),
                "img": entry["img"],
                "title": entry["title"],
                "transcript": entry["transcript"],
                "alt": entry["alt"]
            })
        return json.dumps({
            string: matched_entries
        })

if __name__ == '__main__':
    ''' Setting up the Server with Specified Configuration'''

    server_config = configparser.RawConfigParser()
    env = Environment(loader=FileSystemLoader(''))
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './resources'
        }
    }
    server_config.read('server.conf')
    server_port = server_config.get('Server', 'port')
    server_host = server_config.get('Server', 'host')
    comic_url = server_config.get('xkcd', 'url')
    database_uri = server_config.get('Database', 'database_uri')
    configuration = {
        'comic_url': comic_url,
        'database_uri': database_uri
    }
    cherrypy.config.update({'server.socket_host': server_host})
    cherrypy.config.update({'server.socket_port': int(
        os.environ.get('PORT', server_port)
    )})
    cherrypy.quickstart(Server(configuration), '/', conf)
