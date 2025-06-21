from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] [LOAD_BALANCER] %(message)s')

SUBSTATIONS = ["http://substation1:5002", "http://substation2:5002", "http://substation3:5002"]

@app.route("/route", methods=["POST"])
def route_request():
    vehicle_id = request.json.get("vehicle_id")
    loads = []
    for sub in SUBSTATIONS:
        try:
            metrics = requests.get(f"{sub}/metrics").text
            for line in metrics.splitlines():
                if line.startswith("substation_current_load"):
                    parts = line.split(" ")
                    if len(parts) == 2:
                        load = float(parts[1])
                        loads.append((sub, load))
                        logging.debug(f"Substation {sub} has load {load}")
        except Exception as e:
            logging.error(f"Error contacting {sub}: {e}")

    if not loads:
        return jsonify({"error": "No substation available"}), 503

    target = min(loads, key=lambda x: x[1])[0]
    logging.info(f"Routing vehicle {vehicle_id} to {target}")
    try:
        res = requests.post(f"{target}/charge", json={"vehicle_id": vehicle_id})
        return jsonify({"status": "Charging started", "substation": target}), 200
    except Exception as e:
        logging.error(f"Failed to forward request to {target}: {e}")
        return jsonify({"error": "Failed to forward request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)