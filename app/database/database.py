from pymongo import MongoClient

from app.config import settings


def insert_summary_in_db(key, summary):
    mongodb_client = MongoClient(settings.database_url)
    db = mongodb_client[settings.database_name]
    db["summaries"].insert_one({
        "_id": key,
        "summary": {
            "fileName": summary["fileName"],
            "data": summary["data"]
        }
    })


def find_one_summary_in_db(key):
    mongodb_client = MongoClient(settings.database_url)
    db = mongodb_client[settings.database_name]
    return db["summaries"].find_one({"_id": key})


def find_all_summaries_in_db():
    mongodb_client = MongoClient(settings.database_url)
    db = mongodb_client[settings.database_name]
    return list(db["summaries"].find())
