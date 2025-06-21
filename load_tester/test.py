import requests
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [TEST] %(message)s')

CHARGE_ENDPOINT = "http://localhost:5010/charge"

def simulate_vehicle(i):
    logging.info(f"Vehicle {i} sending charge request")
    res = requests.post(CHARGE_ENDPOINT, json={"vehicle_id": f"EV-{i}"})
    logging.info(f"Vehicle {i} response: {res.json()}")

threads = [threading.Thread(target=simulate_vehicle, args=(i,)) for i in range(50)]

for t in threads:
    t.start()
    time.sleep(0.5)
for t in threads:
    t.join()