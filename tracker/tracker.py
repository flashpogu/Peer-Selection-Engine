import time

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory peer registry
# peer_id -> { address, port, last_seen }
peers = {}

# ----------------------------
# Register / heartbeat endpoint
# ----------------------------


@app.route("/register", methods=["POST"])
def register_peer():
    try:
        data = request.get_json()

        print("Incoming data:", data)

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        peer_id = data.get("peer_id")
        ip = data.get("ip")
        port = data.get("port")

        if not peer_id or not ip or not port:
            return jsonify({"error": "Missing fields"}), 400

        peers[peer_id] = {
            "ip": ip,
            "port": port,
            "last_seen": time.time()
        }

        return jsonify({"status": "registered"})

    except Exception as e:
        print("ERROR in /register:", e)
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Get peer list
# ----------------------------
@app.route("/peers", methods=["GET"])
def get_peers():
    return jsonify(peers)


# ----------------------------
# Health check
# ----------------------------
@app.route("/")
def health():
    return {"tracker": "running", "peer_count": len(peers)}


if __name__ == "__main__":
    print("🚀 Tracker running on http://localhost:8000")
    app.run(host="0.0.0.0", port=8000)
