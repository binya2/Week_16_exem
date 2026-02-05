import json
from pathlib import Path

from pymongo import MongoClient

from app.config import settings


#########################################################################
# Database Connection Logic
#########################################################################

class Database:
    client: MongoClient = None


db = Database()


def get_database():
    return db.client[settings.DATABASE_NAME]


def connect_to_mongo():
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
    fail_name = settings.COLLECTION
    folder = fail_name.split(".")[0]
    if db.client[mongo_db][folder].count_documents({}) == 0:
        print(f"Running seed for: {folder}.")
        data = load_json_file(fail_name)
        if data:
            db.client[mongo_db][folder].insert_many(data)
            print("seeded successfully.")
    else:
        print(f"{folder} collection is not empty. Skipping.")

    print("Seeding process completed.")
