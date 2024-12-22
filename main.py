import subprocess

# Run Uvicorn in the background
uvicorn_process = subprocess.Popen(["uvicorn", "api_keybin_enaza:app", "--reload"])

# Run enaza.py after Uvicorn starts
enaza_process = subprocess.Popen(["python3", "enaza.py", "enaza_k.py"])

# Optionally, wait for both processes to finish (if needed)
uvicorn_process.wait()
enaza_process.wait()

