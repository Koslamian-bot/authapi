# 🚀 FastAPI + MongoDB Advanced CRUD with JWT Authentication

## 📌 Overview

This project demonstrates a complete backend system using:

* FastAPI
* MongoDB
* JWT Authentication
* Basic HTML frontend (optional)

It starts from **basic CRUD** and evolves into a **secure, production-style CRUD API** with:

* Pagination
* Search
* Partial updates (PATCH)
* Soft delete
* Authentication (JWT)
* Authorization (owner-based access)

---

## 🧱 Project Structure

```
social_app/
 ├── main.py
 ├── database.py
 ├── models.py
 ├── auth.py
 ├── routes/
 │     ├── user_routes.py
 │     └── post_routes.py
 ├── templates/
 │     └── index.html
```

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pymongo python-jose passlib[bcrypt]
```

### 2. Run Server

```bash
uvicorn main:app --reload
```

---

## 🗄️ Database Connection

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["social_db"]

user_collection = db["users"]
post_collection = db["posts"]
```

---

## 🧠 Models (Pydantic)

```python
from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Post(BaseModel):
    title: str
    content: str

class UpdatePost(BaseModel):
    title: str | None = None
    content: str | None = None
```

---

# 🔹 BASIC CRUD

## Create User

```python
@router.post("/users")
def create_user(user: User):
    data = user.dict()
    result = user_collection.insert_one(data)
    return {"user_id": str(result.inserted_id)}
```

---

## Get Users (Basic)

```python
@router.get("/users")
def get_users():
    users = list(user_collection.find())
    return users
```

---

# 🚀 ADVANCED CRUD FEATURES

---

## 🔍 Pagination + Search

```python
@router.get("/users")
def get_users(skip: int = 0, limit: int = 5, name: str = ""):

    query = {"is_deleted": False}

    if name != "":
        query["name"] = {"$regex": name}

    users = list(
        user_collection.find(query).skip(skip).limit(limit)
    )

    return users
```

### Features:

* `skip` → offset
* `limit` → number of records
* `name` → search filter

---

## ⚡ Partial Update (PATCH)

```python
@router.patch("/users/{id}")
def update_user(id: str, data: dict):

    update_data = {k: v for k, v in data.items() if v is not None}

    user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
```

### Why PATCH?

* Updates only given fields
* Prevents overwriting entire document

---

## 🧾 Soft Delete

```python
@router.delete("/users/{id}")
def delete_user(id: str):

    user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"is_deleted": True}}
    )
```

### Benefits:

* Data recovery possible
* Audit friendly
* Safer than hard delete

---

# 🔐 JWT AUTHENTICATION

---

## Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
```

---

## Create JWT Token

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## Decode Token

```python
from jose import JWTError

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

---

## Get Current User (Dependency)

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(401, "Invalid token")

    return payload
```

---

# 👤 AUTH ROUTES

---

## Register

```python
@router.post("/register")
def register(user: UserRegister):

    existing = user_collection.find_one({"email": user.email})

    if existing:
        raise HTTPException(400, "User exists")

    data = user.dict()
    data["password"] = hash_password(user.password)

    user_collection.insert_one(data)

    return {"message": "User created"}
```

---

## Login

```python
@router.post("/login")
def login(user: UserLogin):

    db_user = user_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(400, "Invalid email")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(400, "Wrong password")

    token = create_access_token({
        "user_id": str(db_user["_id"])
    })

    return {"access_token": token}
```

---

# 🧾 POSTS WITH AUTHORIZATION

---

## Create Post (Protected)

```python
@router.post("/posts")
def create_post(post: Post, user=Depends(get_current_user)):

    new_post = post.dict()

    new_post["owner_id"] = user["user_id"]
    new_post["created_at"] = str(datetime.now())
    new_post["is_deleted"] = False

    result = post_collection.insert_one(new_post)

    return {"post_id": str(result.inserted_id)}
```

---

## Update Post (Owner Only)

```python
@router.patch("/posts/{id}")
def update_post(id: str, data: UpdatePost, user=Depends(get_current_user)):

    post = post_collection.find_one({"_id": ObjectId(id)})

    if post["owner_id"] != user["user_id"]:
        raise HTTPException(403, "Not allowed")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    post_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
```

---

## Delete Post (Soft Delete + Owner Check)

```python
@router.delete("/posts/{id}")
def delete_post(id: str, user=Depends(get_current_user)):

    post = post_collection.find_one({"_id": ObjectId(id)})

    if post["owner_id"] != user["user_id"]:
        raise HTTPException(403, "Not allowed")

    post_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"is_deleted": True}}
    )
```

---

# 🌐 Frontend Usage (Token Example)

```javascript
fetch("/posts", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN"
    },
    body: JSON.stringify({
        title: "Hello",
        content: "World"
    })
});
```

---

# 🧬 Key Concepts Summary

| Concept       | Meaning                   |
| ------------- | ------------------------- |
| Pagination    | Control data size         |
| Search        | Filter results            |
| PATCH         | Partial update            |
| Soft Delete   | Safe deletion             |
| JWT           | Secure authentication     |
| Dependency    | Inject user automatically |
| Authorization | Restrict access           |

---

# ✅ Outcome

This project demonstrates:

* Clean backend architecture
* Secure authentication flow
* Real-world CRUD practices
* Interview-ready implementation

---
