import bcrypt
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import date
from bson import ObjectId

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["skillspark"]

users_collection = db["users"]
mindmaps_collection = db["mindmaps"]
topics_collection = db["topics"]
contests_collection = db["contests"]
folders_collection = db["folders"]
achievements_collection = db["achievements"]
streaks_collection = db["streaks"]
learns_collection = db["learns"]
histories_collection = db["histories"]

async def create_user(username, email, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {"username": username, "email": email, "password": hashed_pw}
    await users_collection.insert_one(user)

async def authenticate_user(username, password):
    user = await users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True
    return False

# async def create_contest(creator, name, start, end, members, description):
#     contest_data = {
#         "contest_name": name,
#         "creator_id": creator,
#         "created_date": date.today(),
#         "start_date": start,
#         "final_date": end,
#         "mindmap_ids": [],
#         "participant_ids": members,
#         "description": description
#     }
#     await contests_collection.insert_one(contest_data)
    
def run_async(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func(*args))
    loop.close()
    return result

