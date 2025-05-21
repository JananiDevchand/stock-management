from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["stockDB"]
admin_collection = db["admins"]

# Insert admin with hashed password
username = "chandrasekar"
password = "12345"  # Replace with your desired password

hashed_pw = generate_password_hash(password)
admin_collection.insert_one({
    'username': username,
    'password': hashed_pw
})

print(f"✅ Admin '{username}' created successfully.")
