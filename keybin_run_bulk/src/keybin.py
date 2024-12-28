from datetime import datetime
import pymongo
import requests
from dotenv import load_dotenv
import os

def keybin_run():

    dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'venv', '.env')
    load_dotenv(dotenv_path)

    print(" S T A R T")
    # --------------------------------------------------
    mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from the .env file
    com_client = pymongo.MongoClient(mongo_uri)

    mydb = com_client["marketplace"]
    mycol = mydb["keybin"]

    token = os.getenv("TOKEN")
    headers = {"PERSONAL-TOKEN": token}

    keybin_proxy = os.getenv("KEYBIN_PROXY")
    proxies = {"http": keybin_proxy, "https": keybin_proxy}

    # Fetch total number of products
    response = requests.get("https://api.keybin.net/v1/products?embed_listings=true", headers=headers, proxies=proxies)
    print(response.status_code)

    total = response.json()["total"]
    pages = (total + 49) // 50  # Calculate number of pages needed

    print("total pages: ", total)

    products_list = []  # Initialize list to collect products

    for page in range(1, 101):
        print(f"Page: {page}")
        try:  # Fetch products for the current page
            response = requests.get(f"https://api.keybin.net/v1/products?embed_listings=true&take=50&page={page}", headers=headers, proxies=proxies)

            products = response.json()["data"]

            # Process each product
            for product in products:
                try:
                    product["_id"] = int(product["id"])
                    del product["id"]

                    # Collect product data instead of writing to MongoDB line-by-line
                    products_list.append(product)

                except Exception as e:
                    pass
        except Exception as e:
            pass

    # Write all collected products to MongoDB in bulk
    if products_list:
        mycol.drop()  # Clear the collection before writing new data
        mycol.insert_many(products_list)  # Perform a bulk write
        print(f"Inserted {len(products_list)} products into MongoDB.")

    com_client.close()

    print("E N D")

# Ensure this script runs only when executed directly
if __name__ == "__main__":
    keybin_run()

