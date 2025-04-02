from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId
from datetime import date

def to_str_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    bookmark_mindmap: List[str] = []
    achievement_ids: List[str] = []
    user_id: Optional[str] = None

class MindMap(BaseModel):
    mindmap_name: str
    mindmap_description: str
    creator_id: str
    accessibility: bool
    topic_ids: List[str] = []

class Topic(BaseModel):
    topic_name: str
    parent_id: Optional[str] = None
    depth: int
    topic_id: Optional[str] = None

class Contest(BaseModel):
    contest_name: str
    creator_id: str
    created_date: date
    start_date: date
    final_date: date
    mindmap_ids: List[str] = []
    participant_ids: List[str] = [] 

class Folder(BaseModel):
    folder_name: str
    owner_id: str
    accessibility: bool
    mindmap_ids: List[str] = []

class Achievement(BaseModel):
    achievement_id: str
    completion: bool
    pic: str
    user_id: str

class Streak(BaseModel):
    user_id: str
    completion: bool
    curr_streak: int
    max_streak: int
    date: date

class LearnHistory(BaseModel):
    correct: bool
    node_id: int
    root_id: int

class Learn(BaseModel):
    user_id: str
    mindmap_id: str
    score: int
    history: List[LearnHistory] = []

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
