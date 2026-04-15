from pymongo import MongoClient

client = MongoClient("mongodb+srv://raviraahulprof:test123@cluster0.9vh1y.mongodb.net/?appName=Cluster0")

db = client.todo_db

collection_name = db["todo_collection"]