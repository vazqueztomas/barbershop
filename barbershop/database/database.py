import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient
load_dotenv()

uri = os.getenv("MONGODB_URL")
client = MongoClient(uri) # type: ignore
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
haircuts_collection = client["barbershop"]["haircuts"]