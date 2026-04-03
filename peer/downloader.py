import argparse
import requests
import os
import time
import json

from peer.ai_selector import select_best_peer
from peer.config import TRACKER_URL

DOWNLOAD_DIR = "peer/downloads"
RUNTIME_FILE = "peer/runtime.json"
TOTAL_CHUNKS = 10  # adjust


# 🔹 Ensure runtime file exists
def init_runtime():
    if not os.path.exists(RUNTIME_FILE):
        state = {
            "downloaded_chunks": [],
            "total_chunks": TOTAL_CHUNKS,
            "last_peer": None,
            "logs": []
        }
        with open(RUNTIME_FILE, "w") as f:
            json.dump(state, f, indent=2)


def load_state():
    with open(RUNTIME_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(RUNTIME_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_peers():
    try:
        r = requests.get(f"{TRACKER_URL}/peers")
        return r.json()
    except:
        return {}


def download(peer_id):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    init_runtime()

    downloaded = set()

    while len(downloaded) < TOTAL_CHUNKS:
        for chunk_id in range(TOTAL_CHUNKS):
            if chunk_id in downloaded:
                continue

            peers = get_peers()
            result = select_best_peer(peers, peer_id)

            if not result:
                continue

            pid, info = result
            peer_url = f"http://{info['ip']}:{info['port']}"

            try:
                r = requests.get(f"{peer_url}/chunk/{chunk_id}", timeout=3)

                if r.status_code == 200:
                    # Save chunk
                    with open(f"{DOWNLOAD_DIR}/chunk_{chunk_id}", "wb") as f:
                        f.write(r.content)

                    downloaded.add(chunk_id)

                    # 🔥 Update runtime (for UI)
                    state = load_state()
                    state["downloaded_chunks"] = list(downloaded)
                    state["last_peer"] = pid
                    state["logs"].insert(0, f"chunk_{chunk_id} from {pid}")
                    state["logs"] = state["logs"][:10]
                    save_state(state)

                    print(f"⬇️ chunk_{chunk_id} from {pid}")
                    print(f"📊 Progress: {len(downloaded)}/{TOTAL_CHUNKS}")

            except Exception as e:
                continue

        time.sleep(1)

    print("✅ Download complete!")
    reconstruct()


def reconstruct():
    output = os.path.join(DOWNLOAD_DIR, "final_output.mp4")

    chunks = sorted(
        [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith("chunk_")],
        key=lambda x: int(x.split("_")[1])
    )

    with open(output, "wb") as out:
        for chunk in chunks:
            with open(os.path.join(DOWNLOAD_DIR, chunk), "rb") as f:
                out.write(f.read())

    print(f"🎉 File ready: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--peer_id", required=True)

    args = parser.parse_args()

    download(args.peer_id)
