from flask import Flask, send_file, abort
import os
import argparse

app = Flask(__name__)

# Absolute path (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(BASE_DIR, "shared", "chunks")


@app.route("/chunk/<int:chunk_id>")
def get_chunk(chunk_id):
    try:
        file_path = os.path.join(CHUNK_DIR, f"chunk_{chunk_id}")

        print(f"Serving: {file_path}")  # debug

        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            print("File not found")
            return abort(404)

    except Exception as e:
        print("ERROR in uploader:", e)
        return "Internal Server Error", 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)

    args = parser.parse_args()

    print(f"📤 Uploader running on http://localhost:{args.port}")
    print(f"📂 Serving from: {CHUNK_DIR}")

    app.run(host="0.0.0.0", port=args.port)
