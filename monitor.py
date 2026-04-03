import requests
import time
import os
from peer.config import TRACKER_URL


def clear():
    os.system("cls" if os.name == "nt" else "clear")


while True:
    try:
        r = requests.get(f"{TRACKER_URL}/peers")
        peers = r.json()

        clear()
        print("📡 LIVE PEER LIST\n")
        print(f"{'Peer ID':<10} {'IP':<15} {'Port':<6} {'Last Seen':<15}")
        print("-" * 50)

        for pid, info in peers.items():
            print(
                f"{pid:<10} {info['ip']:<15} {info['port']:<6} {round(info['last_seen'],2):<15}")

        if not peers:
            print("No peers connected")

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
