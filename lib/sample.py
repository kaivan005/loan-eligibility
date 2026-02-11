import os
import streamlit as st
from pymongo import MongoClient
from datetime import datetime


def _get_mongo_uri() -> str:
    if "mongo" in st.secrets and "uri" in st.secrets["mongo"]:
        return st.secrets["mongo"]["uri"]
    return os.getenv("MONGO_URI", "")# 🔹 Replace with your MongoDB Atlas connection string
urim = _get_mongo_uri()

# Connect to MongoDB Atlas
client = MongoClient(urim)

# Create / Access Database
db = client["loan-app-data"]

# Create / Access Collection
collection = db["users"]

# Small sample data
user_data = {
    "name": "Kaivan",
    "email": "kaivan@example.com",
    "age": 25,
    "created_at": datetime.utcnow()
}

# Insert data
result = collection.insert_one(user_data)

print("Data inserted successfully ✅")
print("Inserted ID:", result.inserted_id)

# Close connection
client.close()
