import motor.motor_asyncio
import os

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
db = client.get_database("barbershop")
haircuts_collection = db.get_collection("haircuts")



