import argparse
import requests
import os
import time
from peer.ai_selector import select_best_peer
from peer.config import TRACKER_URL

# TRACKER_URL = "http://127.0.0.1:8000"
DOWNLOAD_DIR = "peer/downloads"
TOTAL_CHUNKS = 10  # adjust


def get_peers():
    try:
        r = requests.get(f"{TRACKER_URL}/peers")
        return r.json()
    except:
        return {}


def download(peer_id):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
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
                    with open(f"{DOWNLOAD_DIR}/chunk_{chunk_id}", "wb") as f:
                        f.write(r.content)

                    downloaded.add(chunk_id)
                    print(f"⬇️ chunk_{chunk_id} from {pid}")
                    print(f"📊 Progress: {len(downloaded)}/{TOTAL_CHUNKS}")

            except:
                continue

        time.sleep(1)

# NORMAL
    # while len(downloaded) < TOTAL_CHUNKS:
    #     peers = get_peers()

    #     for pid, info in peers.items():
    #         if pid == peer_id:
    #             continue

    #         peer_url = f"http://{info['ip']}:{info['port']}"

    #         for chunk_id in range(TOTAL_CHUNKS):
    #             if chunk_id in downloaded:
    #                 continue

    #             try:
    #                 r = requests.get(f"{peer_url}/chunk/{chunk_id}", timeout=3)

    #                 if r.status_code == 200:
    #                     with open(f"{DOWNLOAD_DIR}/chunk_{chunk_id}", "wb") as f:
    #                         f.write(r.content)

    #                     downloaded.add(chunk_id)
    #                     print(f"chunk_{chunk_id} from {pid}")

    #             except:
    #                 continue

    #     time.sleep(1)

    print("Download complete!")
    reconstruct()


def reconstruct():
    output = os.path.join(DOWNLOAD_DIR, "final_output.mp4")

    chunks = sorted(
        [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith("chunk_")],
        key=lambda x: int(x.split("_")[1])
    )

    with open(output, "wb") as out:
        for chunk in chunks:
            if chunk.startswith("chunk_"):
                with open(os.path.join(DOWNLOAD_DIR, chunk), "rb") as f:
                    out.write(f.read())

    print(f"🎉 File ready: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--peer_id", required=True)

    args = parser.parse_args()

    download(args.peer_id)
