import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
load_dotenv()

# MONGO_URI = os.getenv("MONGODB_URL")
# print(MONGO_URI)

# def database_connection():
#     try:
#         client = MongoClient(MONGO_URI)
#         db = client["barbershop"]
#         haircuts_db = db["haircuts"]
#         return haircuts_db
#     except Exception as e:
#         print(f"An error occurred while connecting to the database: {e}")
#         return NotImplementedError
    
# haircuts_collection = database_connection()

uri = os.getenv("MONGODB_URL")
client = MongoClient(uri)
print(client)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
haircuts_collection = client["barbershop"]["haircuts"]