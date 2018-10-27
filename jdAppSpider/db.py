import pymongo
from settings import *


class MongodbClient:
    def __init__(self, db_name, collection_name, host=HOST, port=PORT):
        """

        :param name: 集合名称
        :param host:
        :param port:
        """
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]
