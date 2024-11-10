from datetime import datetime
import pymongo
import requests

print(" S T A R T" )
#-------------------------------------------------------------------------------------------

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb://marketplace:rEUlay_7Q9Q2hPjWPadxHMsD@mongo.opl.infrapu.sh:27017/?authSource=marketplace")

mydb = myclient["marketplace"]
mycol = mydb["keybin"]

headers = {"PERSONAL-TOKEN":"4aNI~ZCqv17i+6!)bBj="}

proxies = {"http": "http://opl:eo1muuShifee5yeGhaep@back-hz-2.opl.infrapu.sh:3128",
           "https": "http://opl:eo1muuShifee5yeGhaep@back-hz-2.opl.infrapu.sh:3128", }
#-------------------------------------------------------------------------------------------

# Fetch total number of products
response = requests.get("https://api.keybin.net/v1/products?embed_listings=true", headers = headers, proxies=proxies)
print(response.status_code)
#print(response.text)

total = response.json()["total"]
pages = (total + 49) // 50 # Calculate number of pages needed

for page in range(1, 33 ):
  print(f"Page: {page}")
  try: # Fetch products for the current page
    response = requests.get(f"https://api.keybin.net/v1/products?embed_listings=true&take=50&page={page}", headers=headers, proxies=proxies)

    products = response.json()["data"]

    # Process each product
    for product in products:
      try:

        product["_id"] = int(product["id"])
        del product["id"]
        _id = product["_id"]
        image = product.get("image")
        image2 = product.get("image2")
        image3 = product.get("image3")
        name = product["name"]
        region = product.get("region")
        # Update or insert product in the dump collection
        mycol.replace_one({"_id": _id}, product, upsert=True)
        # Filter listings based on conditions
        listings = [listing for listing in product["listings"] if listing["isActive"] and listing["activeStock"] > 0 and listing["price"]["minOrderQty"] is None]
        listings.sort(key=lambda x: x["price"]["price"])
        active_stock = sum(listing["activeStock"] for listing in listings) 
        price = listings[0]["price"]["price"] if listings else 0
       
 # Prepare document to be inserted or updated in the ozon collection

        now = { 
          "_id": _id, 
          "name": name, 
          "price": price, 
          "active": active_stock > 3, 
          "image": image, 
          "image2": image2, 
         "image3": image3,  
}
      except Exception as e:
        pass
  except Exception as e:
    pass

myclient.close()

print ("E N D")

