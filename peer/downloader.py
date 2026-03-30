# isort: skip_file
# fmt: off

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

sys.path.insert(0, PROJECT_ROOT)

# --------------------------------------------------
# Now ALL other imports are safe
# --------------------------------------------------
import requests
import time

from peer_model import PeerNode
from src.ml.predict import predict_peer_score

# --------------------------------------------------
# Constants
# --------------------------------------------------
TRACKER_URL = "http://localhost:8000"
DOWNLOAD_DIR = os.path.join(BASE_DIR, "shared", "downloads")


def get_peers():
    resp = requests.get(f"{TRACKER_URL}/peers")
    resp.raise_for_status()
    return resp.json()


def get_peer_chunks(peer):
    url = f"http://{peer.address}:{peer.port}/chunks"
    start = time.time()
    resp = requests.get(url)
    latency = (time.time() - start) * 1000

    resp.raise_for_status()
    peer.latency = latency
    peer.availability = len(resp.json()) / 10
    return resp.json()


def download_chunk(peer, chunk_name):
    chunk_id = chunk_name.split("_")[1]
    url = f"http://{peer.address}:{peer.port}/chunk/{chunk_id}"

    start = time.time()
    resp = requests.get(url)
    duration = time.time() - start

    resp.raise_for_status()

    size = len(resp.content)
    peer.upload_rate = size / max(duration, 0.001)
    peer.reliability = min(1.0, peer.reliability + 0.05)

    out_path = os.path.join(DOWNLOAD_DIR, chunk_name)
    with open(out_path, "wb") as f:
        f.write(resp.content)

    print(f"⬇️  {chunk_name} from {peer.peer_id} | {peer.upload_rate:.1f} B/s")


def rank_peers(peers):
    for peer in peers:
        peer.score = predict_peer_score(peer)
    return sorted(peers, key=lambda p: p.score, reverse=True)


def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    raw_peers = get_peers()
    peers = [
        PeerNode(pid, info["address"], info["port"])
        for pid, info in raw_peers.items()
    ]

    downloaded = set(os.listdir(DOWNLOAD_DIR))

    # for peer in peers:
    #     try:
    #         chunks = get_peer_chunks(peer)
    #     except Exception:
    #         continue

    #     missing = [c for c in chunks if c not in downloaded]
    #     if not missing:
    #         continue

    #     for best_peer in rank_peers(peers):
    #         try:
    #             download_chunk(best_peer, missing[0])
    #             downloaded.add(missing[0])
    #             break
    #         except Exception:
    #             best_peer.reliability *= 0.9

    while True:
        all_missing = set()

        for peer in peers:
            try:
                chunks = get_peer_chunks(peer)
                all_missing.update(chunks)
            except Exception:
                continue

        all_missing = [c for c in all_missing if c not in downloaded]

        if not all_missing:
            print("✅ All chunks downloaded")
            break

        ranked_peers = rank_peers(peers)

        for chunk in all_missing:
            for best_peer in ranked_peers:
                try:
                    download_chunk(best_peer, chunk)
                    downloaded.add(chunk)
                    break
                except Exception:
                    best_peer.reliability *= 0.9



if __name__ == "__main__":
    main()
