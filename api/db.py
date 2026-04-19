import os
import certifi
from datetime import datetime, timezone
from pymongo import MongoClient

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGODB_URI"], tlsCAFile=certifi.where())
    return _client[os.environ.get("MONGODB_DB", "genztech")]


def get_leads():
    return get_db()["leads"]


def upsert_lead(phone: str, update: dict):
    """Insert or update a lead document by phone number."""
    leads = get_leads()
    now = datetime.now(timezone.utc)
    leads.update_one(
        {"phone": phone},
        {
            "$set": {**update, "last_message_at": now},
            "$setOnInsert": {"phone": phone, "created_at": now},
        },
        upsert=True,
    )


def get_lead(phone: str):
    return get_leads().find_one({"phone": phone})


def insert_test_lead():
    """Run once to verify DB connection. Delete from DB after confirming."""
    from datetime import timezone
    upsert_lead(
        phone="whatsapp:+910000000000",
        update={
            "name": "Test Student",
            "class_level": "12th",
            "interest": "AI & Tech",
            "city": "Pune",
            "stage": "completed",
            "booking_status": "pending",
        },
    )
    lead = get_lead("whatsapp:+910000000000")
    print(f"[DB TEST] Lead inserted: {lead}")
    return lead


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    insert_test_lead()
