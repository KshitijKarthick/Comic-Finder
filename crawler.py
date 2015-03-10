import server
from server import Database
import configparser

if __name__ == '__main__':
    ''' Script to run the Crawler '''

    server_config = configparser.RawConfigParser()
    server_config.read('server.conf')
    database_url=server_config.get('Database', 'database_url')
    database_port=server_config.get('Database', 'database_port')
    database = Database(database_url,int(database_port))
    database.get_data()
