import os
from dotenv import load_dotenv
import uvicorn
from api_keybin_enaza import run_api

# Define the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'venv', '.env')

if __name__ == "__main__":
    # Start the FastAPI server
    instance = os.getenv("instance")
    
    if instance == "api":
        run_api()
        print("api DONE!!!")
    elif instance == "keybin":
        print("keybin")
    else:
        print("Unknown instance")

