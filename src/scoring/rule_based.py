def compute_peer_score(peer, weights):
    """
    Compute peer quality score using weighted metrics
    """

    score = (
        weights["upload"] * peer.upload_rate +
        weights["reliability"] * peer.reliability +
        weights["availability"] * peer.availability -
        weights["latency"] * peer.latency
    )

    return score
