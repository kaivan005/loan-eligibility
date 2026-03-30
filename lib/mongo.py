from datetime import datetime

import certifi
import streamlit as st
from pymongo import MongoClient


MONGO_URI = st.secrets["MONGO_URI"]
DATABASE_NAME = st.secrets["DATABASE_NAME"]
COLLECTION_NAME = st.secrets["COLLECTION_NAME"]
USERS_COLLECTION_NAME = st.secrets.get("USERS_COLLECTION_NAME", "users")
LOGIN_AUDIT_COLLECTION_NAME = st.secrets.get("LOGIN_AUDIT_COLLECTION_NAME", "login_audit")
FEEDBACK_COLLECTION_NAME = st.secrets.get("FEEDBACK_COLLECTION_NAME", "feedback")


client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
users_collection = db[USERS_COLLECTION_NAME]
login_audit_collection = db[LOGIN_AUDIT_COLLECTION_NAME]
feedback_collection = db[FEEDBACK_COLLECTION_NAME]

try:
    users_collection.create_index("email", unique=True)
except Exception:
    pass


def save_eligibility(payload: dict):
    """
    Saves eligibility result to MongoDB Atlas
    Returns inserted document ID
    """

    payload["created_at"] = datetime.utcnow()

    result = collection.insert_one(payload)

    return str(result.inserted_id)

def get_all_eligibility():
    """
    Returns all eligibility records
    """
    return list(collection.find().sort("created_at", -1))


def get_eligibility_by_date_range(start_at: datetime, end_at: datetime) -> list[dict]:
    """Returns eligibility records where created_at is within [start_at, end_at]."""
    return list(
        collection.find(
            {
                "created_at": {
                    "$gte": start_at,
                    "$lte": end_at,
                }
            }
        ).sort("created_at", -1)
    )


def find_user_by_email(email: str) -> dict | None:
    return users_collection.find_one({"email": email.strip().lower()})


def create_user(full_name: str, email: str, password_hash: str, gender: str, marital: str, no_of_dependents: int, self_employed: str, applicant_income: str, co_applicant_income: str, credit_history: str, property_area: str) -> None:
    users_collection.insert_one(
        {
            "full_name": full_name.strip(),
            "email": email.strip().lower(),
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
            "last_login_at": None,
            "session_token": None,
            "gender": gender,
            "marital": marital,
            "no_of_dependents": no_of_dependents,
            "self_employed": self_employed,
            "applicant_income": applicant_income,
            "co_applicant_income": co_applicant_income,
            "credit_history": credit_history,
            "property_area": property_area,
        }
    )


def update_user_last_login(email: str) -> None:
    users_collection.update_one(
        {"email": email.strip().lower()},
        {"$set": {"last_login_at": datetime.utcnow()}},
    )


def update_user_session_token(email: str, token: str | None) -> None:
    users_collection.update_one(
        {"email": email.strip().lower()},
        {"$set": {"session_token": token}},
    )


def find_user_by_session_token(token: str) -> dict | None:
    return users_collection.find_one({"session_token": token})


def get_eligibility_for_user(email: str) -> list[dict]:
    return list(
        collection.find({"user_email": email.strip().lower()}).sort("created_at", -1)
    )


def add_feedback(user_email: str, user_name: str, rating: int, message: str) -> None:
    feedback_collection.insert_one(
        {
            "user_email": user_email.strip().lower(),
            "user_name": user_name.strip(),
            "rating": rating,
            "message": message.strip(),
            "created_at": datetime.utcnow(),
        }
    )


def get_feedback_for_user(user_email: str) -> list[dict]:
    return list(
        feedback_collection.find({"user_email": user_email.strip().lower()}).sort("created_at", -1)
    )


def get_all_feedback() -> list[dict]:
    return list(feedback_collection.find().sort("created_at", -1))


def get_feedback_by_date_range(start_at: datetime, end_at: datetime) -> list[dict]:
    return list(
        feedback_collection.find(
            {
                "created_at": {
                    "$gte": start_at,
                    "$lte": end_at,
                }
            }
        ).sort("created_at", -1)
    )


def get_all_users() -> list[dict]:
    return list(
        users_collection.find(
            {}, {"password_hash": 0, "session_token": 0}
        ).sort("created_at", -1)
    )


def get_users_by_date_range(start_at: datetime, end_at: datetime) -> list[dict]:
    return list(
        users_collection.find(
            {
                "created_at": {
                    "$gte": start_at,
                    "$lte": end_at,
                }
            },
            {"password_hash": 0, "session_token": 0},
        ).sort("created_at", -1)
    )


def record_login_event(identifier: str, role: str, success: bool) -> None:
    login_audit_collection.insert_one(
        {
            "identifier": identifier.strip().lower(),
            "role": role,
            "success": success,
            "created_at": datetime.utcnow(),
        }
    )
