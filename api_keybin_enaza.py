import pymongo
import json
from dotenv import load_dotenv #1
import os  
from fastapi import FastAPI

# -- CONNECTION TO MONGO DB /   SWITCH from loc to comany mongo
load_dotenv()  # Load environment variables from .env

mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from the .env file
com_client = pymongo.MongoClient(mongo_uri) # Connect to MongoDB
#com_client = pymongo.MongoClient("mongodb://marketplace:rEUlay_7Q9Q2hPjWPadxHMsD@mongo.opl.infrapu.sh:27017/?authSource=marketplace")

#loc_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = com_client["marketplace"]
#db = loc_client["marketplace"]

col = db["keybin"]

# ----  E N A Z A ------------------------------------------

def search_enaza(word):
    db.enaza_search.create_index([("name", "text")]) # Create a text index on the "name" field

    res_enaza = db.enaza_search.find(   
        {"$text": {"$search": word}},
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).limit(21)

    #search_table = []
    api_table_enaza = []
    for document in res_enaza:
        api_table_enaza.append({"product_id ": document["product_id"], "name": document["name"], "provider ":"enaza"})
#       api_table.append({"id": document['_id'], "name": document["name"]})
#       search_table.append(document)

    return api_table_enaza

#-   K E Y B I N -----------------------------------------------------------

def search_keybin(word):    
    db.keybin.create_index([("name", "text")]) #Create a text index on the "name" field
    
    res_prices = db.keybin.find(
        {"$text": {"$search": word}}, 
        {"score": {"$meta": "textScore"}}
    ).sort(
        [("score", {"$meta": "textScore"})]
    ).limit(1000)

    search_table = []
    api_table = []
    for document in res_prices:
        api_table.append({"id": document['_id'], "name": document["name"], "provider ": "keybin"})
        search_table.append(document)

    return  api_table

#----   T O T A L      S E A R C H  ----------------------------------------------------------------------------

def  search_total(word):
    api_table_total = []
    for doc in search_keybin(word):
        api_table_total.append(doc)
   
    for doc in search_enaza(word):
        api_table_total.append(doc)

    return  api_table_total

# ---    A P I  on name --------------------------------------------

app = FastAPI()

@app.get("/search_name/{word}")
async def search_game(word: str):
    result = search_total(word)
    return result

# ----  SEARCH ON  ID --------------

def search_id(id):
    query = {"_id" : id}
    doc = col.find(query)
    result  = []
    for item in doc:
        result.append(item)
    return result

name_id = 10000008994
print (search_id(name_id))

# ---- A P I   on id ----------------

@app.get("/search_id/{id}")
async def search_game_id(id: int):
    result = search_id(id)
    return result

#---------------------------------------------------------------------y


# --- HOW  TO  RUN  THIS FILE ----------------

# wget -qO- http://127.0.0.1:8000/search_name/star
#  wget -qO- http://127.0.0.1:8000/search_name/Suns | jq -c '.[]'
# uvicorn api_search_keybin:app --reload
