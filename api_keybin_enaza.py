import pymongo
import json
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn

# -- CONNECTION TO MONGO DB / SWITCH from loc to company mongo
load_dotenv()  # Load environment variables from .env

mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from the .env file
com_client = pymongo.MongoClient(mongo_uri)  # Connect to MongoDB

db = com_client["marketplace"]
col = db["keybin"]

# ---- E N A Z A ------------------------------------------
def search_enaza(word):
    db.enaza_search.create_index([("name", "text")])  # Create a text index on the "name" field
    res_enaza = db.enaza_search.find(
        {"$text": {"$search": word}},
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).limit(21)

    api_table_enaza = []
    for document in res_enaza:
        api_table_enaza.append({"product_id ": document["product_id"], "name": document["name"], "provider ": "enaza"})

    return api_table_enaza

# ---- K E Y B I N -----------------------------------------------------------
def search_keybin(word):
    db.keybin.create_index([("name", "text")])  # Create a text index on the "name" field
    res_prices = db.keybin.find(
        {"$text": {"$search": word}},
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).limit(1000)

    api_table = []
    for document in res_prices:
        api_table.append({"id": document["_id"], "name": document["name"], "provider ": "keybin"})

    return api_table

# ---- TOTAL SEARCH ----------------------------------------------------------------------------
def search_total(word):
    api_table_total = []
    api_table_total.extend(search_keybin(word))
    api_table_total.extend(search_enaza(word))
    return api_table_total

# ---- SEARCH ON ID --------------
def search_id(id):
    query = {"_id": id}
    doc = col.find(query)
    result = [item for item in doc]
    return result

# --- API SETUP --------------------------------------------
app = FastAPI()

@app.get("/search_name/{word}")
async def search_game(word: str):
    result = search_total(word)
    return result

@app.get("/search_id/{id}")
async def search_game_id(id: int):
    result = search_id(id)
    return result

# --- RUN THE API -------------------------------------------
def run_api():
    print("Starting the API...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

#run_api()
