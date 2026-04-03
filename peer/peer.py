import argparse
import requests
import threading
import time
import os
from peer.config import TRACKER_URL

# TRACKER_URL = "http://127.0.0.1:8000"


def register(peer_id, port):
    data = {
        "peer_id": peer_id,
        "ip": "127.0.0.1",
        "port": port
    }

    try:
        r = requests.post(f"{TRACKER_URL}/register", json=data)
        print("Register response:", r.status_code, r.text)
    except Exception as e:
        print("Register failed:", e)


def heartbeat(peer_id):
    while True:
        try:
            requests.post(f"{TRACKER_URL}/heartbeat",
                          json={"peer_id": peer_id})
        except:
            pass
        time.sleep(10)


def start_uploader(port):
    os.system(f"python peer/uploader.py --port {port}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--peer_id", required=True)
    parser.add_argument("--port", type=int, required=True)

    args = parser.parse_args()

    register(args.peer_id, args.port)

    threading.Thread(
        target=heartbeat,
        args=(args.peer_id,),
        daemon=True
    ).start()

    print(f"Peer {args.peer_id} running (no download yet)")

    start_uploader(args.port)


if __name__ == "__main__":
    main()
