from keybin import keybin_run

#if __name__ == "__main__":
#    keybin_run()



import os
import time  # Import the time module for sleep functionality
from dotenv import load_dotenv
#from enaza import enaza_run


from keybin import keybin_run


dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'venv', '.env')
load_dotenv(dotenv_path)

def main():
    while True:  # Infinite loop to repeatedly execute the script
        instance = os.getenv("instance")
        if instance == "keybin":
            keybin_run()
            print("keybin DONE!!!")
        elif instance == "enaza":
            print("enaza")
        else:
            print("Unknown instance")

        # Delay for 1 hour (3600 seconds)
        print("Waiting for 36 sec  before the next execution...")
        time.sleep(36)

if __name__ == "__main__":
    main()


