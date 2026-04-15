from fastapi import APIRouter
from models.model import Todo
from config.database import collection_name
from schema.schemas import group_fetch
from bson import ObjectId


router = APIRouter()

#get method

@router.get("/")
async def get_todos():
    todoss = group_fetch(collection_name.find())
    return todoss



@router.post("/")
async def post_todo(todo:Todo):
    collection_name.insert_one(dict(todo))