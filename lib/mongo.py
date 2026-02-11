from pymongo import MongoClient
from datetime import datetime
import certifi
import os
import streamlit as st
from pymongo import MongoClient
# -----------------------------
# CONFIG
# -----------------------------
MONGO_URI = st.secrets["MONGO_URI"]
DATABASE_NAME = st.secrets["DATABASE_NAME"]
COLLECTION_NAME = st.secrets["COLLECTION_NAME"]

# -----------------------------
# CONNECTION (Singleton Style)
# -----------------------------

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


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
