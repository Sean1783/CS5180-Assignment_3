from pymongo import MongoClient

def connect_to_database():
    DB_NAME = "web_crawler"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database did not connect successfully")

def create_document(db_collection, page_url, page_html, is_target):
    result = db_collection.insert_one({
        "url": page_url,
        "html": page_html,
        "is_target": is_target
    })
    return result.inserted_id