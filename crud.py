import os
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection


def _get_client() -> MongoClient:
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI is not set.")
    return MongoClient(uri)


def get_collection() -> Collection:
    db_name = os.getenv("MONGODB_DB", "astro_journal")
    collection_name = os.getenv("MONGODB_COLLECTION", "food")
    client = _get_client()
    return client[db_name][collection_name]


def ping_db() -> Tuple[bool, str]:
    try:
        client = _get_client()
        client.admin.command("ping")
        return True, "Connected to MongoDB"
    except Exception as e:
        return False, f"MongoDB ping failed: {e}"


def insert_feeding(doc: Dict[str, Any]) -> Optional[str]:
    """
    Inserts a document like:
    { "date": "YYYY-MM-DD", "time": "HH:MM", "name": "...", "amount": "..." }
    Returns inserted_id as string, or None on failure.
    """
    try:
        col = get_collection()
        result = col.insert_one(doc)
        return str(result.inserted_id)
    except Exception:
        return None


def list_feedings(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Returns most recent feedings. Since your schema stores date+time as strings,
    we sort by _id (insertion order) descending, which works well for a log.
    """
    try:
        col = get_collection()
        items = list(col.find({}).sort([("_id", -1)]).limit(limit))
        # Convert ObjectId to string for templates
        for it in items:
            if isinstance(it.get("_id"), ObjectId):
                it["_id"] = str(it["_id"])
        return items
    except Exception:
        return []