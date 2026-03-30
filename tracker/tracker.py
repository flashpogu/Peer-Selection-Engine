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
    data = request.json

    peer_id = data.get("peer_id")
    address = data.get("address")
    port = data.get("port")

    if not peer_id or not address or not port:
        return jsonify({"error": "missing fields"}), 400

    peers[peer_id] = {
        "address": address,
        "port": port,
        "last_seen": datetime.utcnow().isoformat()
    }

    return jsonify({"status": "registered"})


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
