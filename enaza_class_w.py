import os
import json
import requests
import subprocess
import time
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings loaded from environment variables."""
    MONGODB_URL = os.getenv("MONGODB_URL", "")
    MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "marketplace")
    MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "new_enaza")
    PASSPHRASE = os.getenv("PASSPHRASE", "")
    PARTNER_CODE = os.getenv("PARTNER_CODE", "")


class MongoDBClient:
    """MongoDB client wrapper for connecting and managing the database."""
    def __init__(self, url: str, dbname: str):
        self.client = MongoClient(url)
        self.db = self.client[dbname]
        self.collection = self.db[Config.MONGODB_COLLECTION]

    def update_data(self, data: dict, inst: str):
        """Process and update data in the MongoDB collection."""
        c = 1
        for item in data:
            try:
                print(f"Updating {c}/{len(data)} for {inst}...")
                if inst == 'products':
                    item["_id"] = item["sku"]
                    del item["sku"]
                    self.collection.replace_one({"_id": item["_id"]}, item, upsert=True)
                elif inst == 'prices':
                    existing_item = self.collection.find_one({'_id': item["sku"]})
                    if existing_item:
                        print(f"Updating {item['sku']}")
                        self.collection.update_one({'_id': item["sku"]}, {'$set': {'prices': item}})
            except Exception as e:
                print(e)
            c += 1


class FileProcessor:
    """Handles downloading, decrypting, decompressing, and processing files."""
    @staticmethod
    def download_file(url, filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    @staticmethod
    def decrypt_file(encrypted_filename, decrypted_filename, passphrase):
        subprocess.run([
            'openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2',
            '-pass', f'pass:{passphrase}', '-in', encrypted_filename,
            '-out', decrypted_filename
        ])

    @staticmethod
    def decompress_file(compressed_filename):
        subprocess.run(['gzip', '-d', compressed_filename])


class EnazaProcessor:
    """Main processor for handling Enaza product data."""
    def __init__(self, inst: str):
        self.inst = inst
        self.start_time = time.time()

    def process(self):
        url = f'https://rokky-cdn.azureedge.net/partner-catalogs/{Config.PARTNER_CODE}_{self.inst}.json.gz.enc'
        encrypted_filename = f'{Config.PARTNER_CODE}_{self.inst}.json.gz.enc'
        decrypted_filename = f'{Config.PARTNER_CODE}_{self.inst}.json.gz'
        json_filename = f'{Config.PARTNER_CODE}_{self.inst}.json'

        # Download, decrypt, and decompress the file
        print(f'Downloading {url}...')
        FileProcessor.download_file(url, encrypted_filename)
        print(f'Decrypting {encrypted_filename}...')
        FileProcessor.decrypt_file(encrypted_filename, decrypted_filename, Config.PASSPHRASE)
        print('Done decrypting!')
        print(f'Decompressing {decrypted_filename}...')
        FileProcessor.decompress_file(decrypted_filename)
        print('Done decompressing!')

        # Process JSON data
        print(f'Processing {json_filename}...')
        with open(json_filename, 'r') as f:
            data = json.load(f)
            db_client = MongoDBClient(Config.MONGODB_URL, Config.MONGODB_DBNAME)
            db_client.update_data(data, self.inst)

        end_time = time.time()
        execution_time = end_time - self.start_time
        print(f"Execution time: {execution_time} seconds")


# Process data
inst = 'products'
enaza_processor = EnazaProcessor(inst)
enaza_processor.process()

# Retrieve the 3rd document from the "new_enaza" collection
db_client = MongoDBClient(Config.MONGODB_URL, Config.MONGODB_DBNAME)
third_document = db_client.collection.find().skip(2).limit(1)  # Skip first 2 documents, retrieve the 3rd

# Print the 3rd document
for document in third_document:
    print(f"Third document: {document}")

