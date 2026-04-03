from flask import Flask, json, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # allow frontend requests

# 🔹 Tracker URL from env (works for LAN too)
TRACKER_IP = os.getenv("TRACKER_IP", "127.0.0.1").strip()
TRACKER_PORT = 8000
TRACKER_URL = f"http://{TRACKER_IP}:{TRACKER_PORT}"


# 🔹 Serve UI
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# 🔹 Get peer list
@app.route("/api/peers")
def get_peers():
    try:
        r = requests.get(f"{TRACKER_URL}/peers")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})


# 🔹 Status endpoint
@app.route("/api/status")
def status():
    return jsonify({
        "status": "running",
        "tracker": TRACKER_URL,
        "message": "AI Swarm Active"
    })


# 🔹 Optional: health check
@app.route("/health")
def health():
    return jsonify({"ok": True})


@app.route("/api/runtime")
def runtime():
    try:
        with open("peer/runtime.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({})


if __name__ == "__main__":
    print(f"🌐 Dashboard running at http://127.0.0.1:5000")
    print(f"🔗 Connected to tracker at {TRACKER_URL}")
    app.run(host="0.0.0.0", port=5000, debug=True)
