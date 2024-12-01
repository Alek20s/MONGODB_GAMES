import uvicorn
import schedule
import time
import threading
import kebin
import enasa
import api


def renewal():
    enasa.enasa_function()
    kebin.kebin_function()


def start_uvicorn():
    uvicorn.run("api:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    # Start Uvicorn server in a separate thread
    uvicorn_thread = threading.Thread(target=start_uvicorn, daemon=True)
    uvicorn_thread.start()

    # Schedule tasks
    schedule.every(1).minutes.do(renewal)

    while True:
        schedule.run_pending()
        time.sleep(1)

