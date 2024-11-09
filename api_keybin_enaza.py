
import pymongo
import json

from fastapi import FastAPI

#-------------------------------------------------------------
# SWITH from loc to comany mongo

com_client = pymongo.MongoClient("mongodb://marketplace:rEUlay_7Q9Q2hPjWPadxHMsD@mongo.opl.infrapu.sh:27017/?authSource=marketplace")
#loc_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = com_client["marketplace"]
#db = loc_client["marketplace"]

col = db["keybin"]
#------------------------------------------------------------
# E N A Z A
import pymongo
import json

com_client = pymongo.MongoClient("mongodb://marketplace:rEUlay_7Q9Q2hPjWPadxHMsD@mongo.opl.infrapu.sh:27017/?authSource=marketplace")
#client = pymongo.MongoClient("mongodb://localhost:27017/")

db = com_client["marketplace"]

#db = client["mydatabase"]

# Create a text index on the "name" field


def search_enaza(word):
    db.enaza_search.create_index([("name", "text")]) #enaza_search

    # Search for documents matching the word "war" and sort by the textScore
    #word = "mars"
    res_enaza = db.enaza_search.find(   # enaza_search
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
#--------------------------------------------------------


word = "planet"
i =  0
for item  in  search_enaza(word):
   i = i + 1
   print (i)
   print (item)




#------------------------------------------------------------
# Create a text index on the "name" field
#db.keybin.create_index([("name", "text")])

# Search for documents matching the word "war" and sort by the textScore

def search_keybin(word):    
    db.keybin.create_index([("name", "text")])
    
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
#-----------------------------------------------------------------------------
search_result = search_keybin("war")
#-----------------------------------------------------------------------------
def  search_total(word):
    api_table_total = []
    for doc in search_keybin(word):
        api_table_total.append(doc)
   
    for doc in search_enaza(word):
        api_table_total.append(doc)

    return  api_table_total


#-----------------------------------------------

# printing search result:
#i =  0 
#for item  in search_result:
#   i = i + 1 
#   print (i)
#   print (item)

print ("#-------------------------")

app = FastAPI()

# Define an async function that accepts one argument
@app.get("/search_name/{word}")
async def search_game(word: str):
    result = search_total(word)
    return result

#  SEARCH USING ID

def search_id(id):
    query = {"_id" : id}
    doc = col.find(query)
    result  = []
    for item in doc:
        result.append(item)
    return result

name_id = 10000008994
print (search_id(name_id))


@app.get("/search_id/{id}")
async def search_game_id(id: int):
    result = search_id(id)
    return result

# RUN

# wget -qO- http://127.0.0.1:8000/search_name/star
#  wget -qO- http://127.0.0.1:8000/search_name/Suns | jq -c '.[]'
# uvicorn api_search_keybin:app --reload
