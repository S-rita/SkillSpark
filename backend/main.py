from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import (
    users_collection, mindmaps_collection, topics_collection, contests_collection,
    folders_collection, achievements_collection, streaks_collection, learns_collection, histories_collection
)
from .models import (
    User, MindMap, Topic, Contest, Folder, Achievement, Streak, Learn, LoginRequest, SignupRequest
)
from bson import ObjectId
from typing import List
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust to limit in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def to_str_id(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode() if isinstance(hashed_password, str) else hashed_password)

# USERS
@app.get("/users/", response_model=List[User])
async def get_users():
    users = await users_collection.find().to_list(100)
    return [to_str_id(user) for user in users]

@app.post("/signup")
async def create_user(user: SignupRequest):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])  

    result = await users_collection.insert_one(user_dict)
    return {"message": "User created", "user_id": str(result.inserted_id)}

@app.post("/login")
async def login(user: LoginRequest):
    existing_user = await users_collection.find_one({"username": user.username})
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "user_id": str(existing_user["_id"])}

# MINDSMAPS
@app.post("/mindmaps/")
async def create_mindmap(mindmap: MindMap):
    result = await mindmaps_collection.insert_one(mindmap.model_dump())
    return {"message": "MindMap created", "mindmap_id": str(result.inserted_id)}

@app.get("/mindmaps/", response_model=List[MindMap])
async def get_mindmaps():
    mindmaps = await mindmaps_collection.find().to_list(100)
    return [to_str_id(mindmap) for mindmap in mindmaps]

# TOPICS
@app.post("/topics/")
async def create_topic(topic: Topic):
    result = await topics_collection.insert_one(topic.model_dump())
    return {"message": "Topic created", "topic_id": str(result.inserted_id)}

@app.get("/topics/", response_model=List[Topic])
async def get_topics():
    topics = await topics_collection.find().to_list(100)
    return [to_str_id(topic) for topic in topics]

# CONTESTS
@app.post("/contests/")
async def create_contest(contest: Contest):
    contest_dict = contest.model_dump()
    print("📦 Received contest:", contest_dict)
    result = await contests_collection.insert_one(contest_dict)
    return {"message": "Contest created", "contest_id": str(result.inserted_id)}

@app.get("/contests/", response_model=List[Contest])
async def get_contests():
    contests = await contests_collection.find().to_list(100)
    return [to_str_id(contest) for contest in contests]

# ACHIEVEMENTS
@app.get("/achievements/")
async def get_achievements():
    achievements = await achievements_collection.find().to_list(100)
    return [to_str_id(achievement) for achievement in achievements]

# STREAKS
@app.get("/streaks/")
async def get_streaks():
    streaks = await streaks_collection.find().to_list(100)
    return [to_str_id(streak) for streak in streaks]

# FOLDERS
@app.post("/folders/")
async def create_folder(folder: Folder):
    folder_dict = folder.model_dump()
    print("📦 Received folder:", folder_dict)
    result = await folders_collection.insert_one(folder_dict)
    return {"message": "Folder created"}

@app.get("/folders/", response_model=List[Folder])
async def get_folders():
    folders = await folders_collection.find().to_list(100)
    return [to_str_id(folder) for folder in folders]
