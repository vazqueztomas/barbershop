import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URL")
client = MongoClient(uri)  # type: ignore
try:
    client.admin.command("ping")
except Exception as e:

haircuts_collection = client["barbershop"]["haircuts"]
