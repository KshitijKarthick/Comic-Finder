#! /usr/bin/env python3
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
            # createIndex same as ensureIndex for mongodb 3 and above
            self.collection.create_index([
                ("title", "text"), ("transcript", "text")
            ])
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

    def search_data(self, string, phrase=True, limit=10, skip=0):
        """ Find the string in the Database """

        # import re
        # from bson import Regex
        # pattern = re.compile(string, re.IGNORECASE)
        # regex = Regex.from_native(pattern)
        # regex.flags ^= re.UNICODE
        # return self.collection.find(
        #     {"transcript": regex}, limit=10, skip=skip
        # ).sort('rank', -1)
        if phrase is True:
            string = "\"" + string + "\""
        return self.collection.find(
            {
                '$text': {
                    '$search': string
                }
            },
            limit=10,
            skip=skip,
        ).sort('rank', -1)

    def get_count(self):
        """ Get the Count of comics """

        # XKCD Perk of 404 Error
        count = self.collection.count()
        if count > 404:
            return count + 1
        else:
            return count

    def increment_rank(self, id):

        data = self.get_comic(id)
        data['rank'] += 1
        self.collection.save(data)
