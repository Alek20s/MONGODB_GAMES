import os
import time  # Import the time module for sleep functionality
from dotenv import load_dotenv
from enaza import enaza_run

load_dotenv()

def main():
    while True:  # Infinite loop to repeatedly execute the script
        instance = os.getenv("instance")
        if instance == "enaza":
            enaza_run()
            print("enaza DONE!!!")
        elif instance == "keybin":
            print("enaza")
        else:
            print("Unknown instance")
        
        # Delay for 1 hour (3600 seconds)
        print("Waiting for 36 sec  before the next execution...")
        time.sleep(36)

if __name__ == "__main__":
    main()

