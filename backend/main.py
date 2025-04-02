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

@app.post("/topics/update_parent")
async def update_topic_parent(data: dict):
    topic_id = data.get("topic_id")
    parent_id = data.get("parent_id")
    
    if not topic_id:
        raise HTTPException(status_code=400, detail="topic_id is required")
        
    # Convert string IDs to ObjectId if necessary
    try:
        topic_id_obj = ObjectId(topic_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid topic_id format")
        
    # Convert parent_id to ObjectId if it's not None
    parent_id_obj = None
    if parent_id:
        try:
            parent_id_obj = ObjectId(parent_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid parent_id format")
    
    # Update the topic with the new parent_id
    result = await topics_collection.update_one(
        {"_id": topic_id_obj},
        {"$set": {"parent_id": parent_id_obj}}
    )
    
    if result.modified_count == 0:
        # Check if the topic exists but wasn't modified
        topic = await topics_collection.find_one({"_id": topic_id_obj})
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
    
    return {"message": "Topic parent updated successfully"}

@app.put("/topics/{topic_id}")
async def update_topic(topic_id: str, topic_update: dict):
    try:
        topic_id_obj = ObjectId(topic_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid topic_id format")
    
    # Convert any string ObjectIds to actual ObjectIds
    if "parent_id" in topic_update and topic_update["parent_id"]:
        try:
            topic_update["parent_id"] = ObjectId(topic_update["parent_id"])
        except:
            raise HTTPException(status_code=400, detail="Invalid parent_id format")
    
    result = await topics_collection.update_one(
        {"_id": topic_id_obj},
        {"$set": topic_update}
    )
    
    if result.modified_count == 0:
        # Check if the document exists
        topic = await topics_collection.find_one({"_id": topic_id_obj})
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
    
    return {"message": "Topic updated successfully"}

@app.get("/topics/", response_model=List[Topic])
async def get_topics():
    topics = await topics_collection.find().to_list(100)
    return [to_str_id(topic) for topic in topics]

# CONTESTS
@app.post("/contests/")
async def create_contest(contest: Contest):
    result = await contests_collection.insert_one(contest.model_dump())
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