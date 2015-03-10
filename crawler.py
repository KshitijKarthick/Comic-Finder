import database
import configparser
import urllib
import json
from urllib import request
from database import Database
def crawl_data(database):
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
                    database.insert_data({
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
    ''' Script to run the Crawler '''

    server_config = configparser.RawConfigParser()
    server_config.read('server.conf')
    database_uri=server_config.get('Database', 'database_uri')
    database = Database(database_uri)
    crawl_data(database)