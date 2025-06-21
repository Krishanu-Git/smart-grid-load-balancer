from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] [CHARGE_SERVICE] %(message)s')

LOAD_BALANCER_URL = "http://load_balancer:5001/route"

@app.route("/charge", methods=["POST"])
def charge_request():
    vehicle_id = request.json.get("vehicle_id")
    logging.info(f"Received charge request from vehicle {vehicle_id}")
    response = requests.post(LOAD_BALANCER_URL, json={"vehicle_id": vehicle_id})
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)