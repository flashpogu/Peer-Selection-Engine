import random
from src.models.peer import Peer


def generate_peers(n):
    peers = []

    for i in range(n):
        peer = Peer(
            peer_id=i,
            upload_rate=random.uniform(50, 500),     # KB/s
            reliability=random.uniform(0.5, 1.0),
            availability=random.uniform(0.3, 1.0),
            latency=random.uniform(20, 200)          # ms
        )
        peers.append(peer)

    return peers
