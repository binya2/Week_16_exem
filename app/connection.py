import json
from pathlib import Path

from pymongo import MongoClient

from config import settings


#########################################################################
# Database Connection Logic
#########################################################################

class Database:
    client: MongoClient = None


db = Database()


def get_database():
    return db.client[settings.DATABASE_NAME]


def connect_to_mongo():
    if db.client:
        print("MongoDB connection already established.")
        return
    print(f"Connecting to MongoDB at: {settings.MONGODB_URL}...")
    try:
        db.client = MongoClient(settings.MONGODB_URL)
        db.client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e


def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")


########################################################################
# Database Seeding Logic
########################################################################

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json_file(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        print(f"Seed file not found: {file_path}")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database():
    print("Checking if database seeding is needed...")
    mongo_db = settings.DATABASE_NAME
    collection = settings.COLLECTION
    fail_name = collection + ".json"
    if db.client[mongo_db][collection].count_documents({}) == 0:
        print(f"Running seed for: {collection}.")
        data = load_json_file(fail_name)
        if data:
            db.client[mongo_db][collection].insert_many(data)
            print("seeded successfully.")
    else:
        print(f"{collection} collection is not empty. Skipping.")

    print("Seeding process completed.")
