import random
from src.ml.predict import predict_peer_score
from src.scoring.rule_based import compute_peer_score


def schedule_peers(peers, weights=None, upload_slots=4):
    # 1. Predict scores using ML
    for peer in peers:
        # peer.score = predict_peer_score(peer)
        peer.score = compute_peer_score(peer, weights)

    # 2. Rank peers
    ranked_peers = sorted(peers, key=lambda p: p.score, reverse=True)

    # 3. Select best peers
    unchoked = ranked_peers[: upload_slots - 1]

    # 4. Optimistic unchoke
    remaining = ranked_peers[upload_slots - 1:]
    if remaining:
        unchoked.append(random.choice(remaining))

    # 5. Apply choke state
    for peer in peers:
        peer.choked = peer not in unchoked

    return unchoked
