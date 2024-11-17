import pymongo
from pymongo import MongoClient

import json
import requests
import subprocess
import os
import time

start_time = time.time()

# S W I T C H local to company mongo

com_client=pymongo.MongoClient("mongodb://marketplace:rEUlay_7Q9Q2hPjWPadxHMsD@mongo.opl.infrapu.sh:27017/?authSource=marketplace")
#loc_client = pymongo.MongoClient("mongodb://localhost:27017/")
#db=loc_client["marketplace"]
db=com_client["marketplace"]


new_collection=db["new_enaza"]

#enaza_sales = db["new_enaza_sales"]
#--------------------------------------------

passphrase='!K9-pE4]"2O|+1v?;lZ1h18!5h?9X31!'
partner_code="OnlineSup"

#--------------------------------------------

def download_file(url,filename):
    with requests.get(url,stream=True) as r:
        r.raise_for_status()
        with open(filename,'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

#------------------------------------------

def decrypt_file(encrypted_filename,decrypted_filename,passphrase):
    subprocess.run([
        'openssl','enc','-d','-aes-256-cbc','-pbkdf2',
        '-pass',f'pass:{passphrase}',
        '-in',encrypted_filename,
        '-out',decrypted_filename
    ])
#--------------------------------------------

def decompress_file(compressed_filename):
    subprocess.run(['gzip', '-d', compressed_filename])

#---------------------------------------------

def process_json_file(filename, inst):
    try:
        print (os.path.exists(f"./{filename}"))
        print (os.path.exists(filename))
        print (os.path.exists(f"../{filename}"))


        with open(filename, 'r') as f:
            data = json.load(f)
#            print (data)

            c=1
            for item in data:
                try:
                    print (f"updating{c}/{len(data)}{inst}...")
                    if inst =='products':
                        item["_id"]=item["sku"]
                        del item["sku"]

                        new_collection.replace_one({"_id":item["_id"]}, item, upsert=True)
                    elif inst=='prices':
                        existing_item=new_collection.find_one({'_id': item["sku"]})
                        if existing_item:
                            print(f"Updating{item['sku']}")
                            new_collection.update_one({'_id': item["sku"]},{'$set':{'prices':item}})
                except Exception as e:
                    print (e)

                c +=1
    except Exception as e:
        print(e)
#---------------------------------------

inst = 'products'
url = f'https://rokky-cdn.azureedge.net/partner-catalogs/{partner_code}_{inst}.json.gz.enc' 
encrypted_filename = f'{partner_code}_{inst}.json.gz.enc'
download_file(url, encrypted_filename)

decrypted_filename=f'{partner_code}_{inst}.json.gz'

json_filename=f'{partner_code}_{inst}.json'

#print (f'Downloading{url}...')

#Downloadencryptedfile

print(f'Decrypting{encrypted_filename}...')

#Decryptfile
decrypt_file(encrypted_filename,decrypted_filename,passphrase)
print('Done!')

# Decompress decrypted file

print  (f'Decompressing {decrypted_filename}...')
decompress_file(decrypted_filename)
print ('Done!')

print (f'Processing {json_filename}...')

process_json_file(json_filename, inst)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


from pymongo import MongoClient

# Connect to MongoDB (replace with your connection string if not local)
client = MongoClient("mongodb://localhost:27017")

# Access a specific database
#db = client["your_database_name"]

# Access a specific collection
#collection = db["your_collection_name"]

#new_collection=db["new_enaza"]

# Retrieve all documents from the collection
data = new_collection.find()

# Print retrieved documents

enaza_data =[]
for document in data:
    enaza_data.append(document)
#    print(document)

print ("to be sure it is downloaded, it's shown its product_id:   ",enaza_data[2]["product_id"])

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

#  I made changes and commited from a server
# second change  2
# git init, git add enaza.py, (make changes), git commit -m "...", git push origin main
# hide variables
