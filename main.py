
import os
import uvicorn
from api_keybin_enaza import run_api

#from script import run_api

if __name__ == "__main__":
    # Start the FastAPI server
#    run_api()


    instance = os.getenv("instance")
    if instance == "api":
        run_api()
        print("api DONE!!!")
    elif instance == "keybin":
        print("keybin")
    else:
        print("Unknown instance")


