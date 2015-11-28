#! /usr/bin/env python3
import re
from bson import Regex
from pymongo import MongoClient


class Database():
    """
        Database Configuration:
        client -> MongoDb client.
        db -> Retrieve the Database.
        collection -> Retrieve the Collection.
    """

    client = ""
    db = ""
    collection = ""

    def __init__(self, database_uri):
        """ Initialization the URL of the comic and transcript """

        try:
            self.client = MongoClient(database_uri)
            self.db = self.client.get_default_database()
            self.collection = self.db.xkcd
        except:
            print("Error Could not Connect with the Database\n")
            print("Make sure connection can be estabilished.")
            exit(-1)

    def insert_data(self, data):
        """ Insert the data into the Collection """

        self.collection.insert(data)

    def get_comic(self, comic_id):
        """ Find comic details for specified comic id """

        return self.collection.find_one({"id": int(comic_id)})

    def search_data(self, string):
        """ Find the string in the Database """

        pattern = re.compile(string, re.IGNORECASE)
        regex = Regex.from_native(pattern)
        regex.flags ^= re.UNICODE
        return self.collection.find({"transcript": regex})

    def get_count(self):
        """ Get the Count of comics """

        return self.collection.count()

    def increment_rank(self, id):

        data = self.get_comic(id)
        data['rank'] += 1
        self.collection.save(data)
