from flask import Flask, request, jsonify, Response
import time
import threading
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] [SUBSTATION] %(message)s')

current_load = 0
lock = threading.Lock()

@app.route("/charge", methods=["POST"])
def charge():
    global current_load
    vehicle_id = request.json.get("vehicle_id")
    logging.info(f"Charging vehicle {vehicle_id}")
    with lock:
        current_load += 1
    time.sleep(2)  # simulate charging delay
    with lock:
        current_load -= 1
    return jsonify({"status": "Charging complete"})

@app.route("/metrics")
def metrics():
    data = (
        "# HELP substation_current_load Current charging load\n"
        "# TYPE substation_current_load gauge\n"
        f"substation_current_load {current_load}\n"
    )
    return Response(data, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)