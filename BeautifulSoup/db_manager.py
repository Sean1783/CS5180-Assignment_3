from pymongo import MongoClient

class DatabaseManager:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name


    def connect_to_database(self):
        DB_NAME = self.db_name
        DB_HOST = "localhost"
        DB_PORT = 27017
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            db = client[DB_NAME]
            return db
        except:
            print("Database did not connect successfully")


    def insert_document(self, page_url, page_html, is_target):
        db_connection = self.connect_to_database()
        collection = db_connection[self.collection_name]
        result = collection.insert_one({
            "url": page_url,
            "html": page_html,
            "is_target": is_target
        })
        return result.inserted_id