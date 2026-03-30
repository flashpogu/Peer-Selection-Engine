class Peer:
    def __init__(self, peer_id, upload_rate, reliability, availability, latency):
        self.peer_id = peer_id

        # Metrics
        self.upload_rate = upload_rate      # KB/s
        self.reliability = reliability      # 0.0 – 1.0
        self.availability = availability    # 0.0 – 1.0
        self.latency = latency              # ms

        # Runtime state
        self.score = 0.0
        self.choked = True

    def __repr__(self):
        status = "CHOKED" if self.choked else "UNCHOKED"
        return f"Peer(id={self.peer_id}, score={self.score:.2f}, {status})"
