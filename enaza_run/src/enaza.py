import pymongo
from pymongo import MongoClient
import json
import requests
import subprocess
import os
import time
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Function definitions remain the same
def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def decrypt_file(encrypted_filename, decrypted_filename, passphrase):
    subprocess.run([
        'openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2',
        '-pass', f'pass:{passphrase}',
        '-in', encrypted_filename,
        '-out', decrypted_filename
    ])

def decompress_file(compressed_filename):
    subprocess.run(['gzip', '-d', compressed_filename])

def process_json_file(filename, inst, new_collection):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            c = 1
            for item in data:
                try:
                    print(f"Updating {c}/{len(data)} {inst}...")
                    if inst == 'products':
                        item["_id"] = item["sku"]
                        del item["sku"]
                        new_collection.replace_one({"_id": item["_id"]}, item, upsert=True)
                    elif inst == 'prices':
                        existing_item = new_collection.find_one({'_id': item["sku"]})
                        if existing_item:
                            print(f"Updating {item['sku']}")
                            new_collection.update_one({'_id': item["sku"]}, {'$set': {'prices': item}})
                except Exception as e:
                    print(e)
                c += 1
    except Exception as e:
        print(e)

# Add the `run` function
def enaza_run():
    start_time = time.time()

    # MongoDB setup
    mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from the .env file
    com_client = pymongo.MongoClient(mongo_uri)
    db = com_client["marketplace"]
    new_collection = db["new_enaza"]

    # Load environment variables
    enaza_passphrase = os.getenv('ENAZA_PASSPHRASE')
    enaza_code = os.getenv("ENAZA_CODE")

    inst = 'products'
    url = f'https://rokky-cdn.azureedge.net/partner-catalogs/{enaza_code}_{inst}.json.gz.enc'
    encrypted_filename = f'{enaza_code}_{inst}.json.gz.enc'
    decrypted_filename = f'{enaza_code}_{inst}.json.gz'
    json_filename = f'{enaza_code}_{inst}.json'
    if os.path.exists(json_filename):
        os.remove(json_filename)  # Automatically overwrite by removing the file

    # File processing workflow
    download_file(url, encrypted_filename)
    print(f"Decrypting {encrypted_filename}...")
    decrypt_file(encrypted_filename, decrypted_filename, enaza_passphrase)
    print("Done!")

    print(f"Decompressing {decrypted_filename}...")
    decompress_file(decrypted_filename)
    print("Done!")

    print(f"Processing {json_filename}...")
    process_json_file(json_filename, inst, new_collection)

    # Print some data to verify
    enaza_data = list(new_collection.find())
    if len(enaza_data) > 2:
        print("Sample product ID:", enaza_data[2]["product_id"])

    # Execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


# to enaza_run
