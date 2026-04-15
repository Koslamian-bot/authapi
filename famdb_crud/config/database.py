from pymongo import MongoClient
import os 
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("MONGODB_PASS")
client = MongoClient(f"mongodb+srv://raviraahulprof:{password}@cluster0.9vh1y.mongodb.net/?appName=Cluster0")

db = client.todo_db

collection_name = db["todo_collection"]