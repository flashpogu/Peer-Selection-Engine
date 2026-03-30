from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(BASE_DIR, "shared", "chunks")


@app.route("/chunks", methods=["GET"])
def list_chunks():
    return jsonify(os.listdir(CHUNK_DIR))


@app.route("/chunk/<int:chunk_id>", methods=["GET"])
def send_chunk(chunk_id):
    chunk_path = os.path.join(CHUNK_DIR, f"chunk_{chunk_id}")

    if not os.path.exists(chunk_path):
        return jsonify({"error": "chunk not found"}), 404

    return send_file(chunk_path, as_attachment=True)


if __name__ == "__main__":
    print("📤 Peer uploader running on http://localhost:9001")
    app.run(host="0.0.0.0", port=9001)
