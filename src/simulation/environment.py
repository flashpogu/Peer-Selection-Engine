import random


def update_peer_metrics(peers):
    """
    Simulate network & peer behavior changes over time
    """

    for peer in peers:
        # Upload rate fluctuates
        peer.upload_rate *= random.uniform(0.9, 1.1)

        # Reliability changes slowly
        peer.reliability += random.uniform(-0.02, 0.02)
        peer.reliability = max(0.0, min(1.0, peer.reliability))

        # Availability improves as peers download
        peer.availability += random.uniform(0.0, 0.03)
        peer.availability = min(1.0, peer.availability)

        # Latency fluctuates
        peer.latency *= random.uniform(0.95, 1.05)
