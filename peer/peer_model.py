class PeerNode:
    def __init__(self, peer_id, address, port):
        self.peer_id = peer_id
        self.address = address
        self.port = port

        # Metrics (initialized conservatively)
        self.upload_rate = 100.0
        self.reliability = 0.8
        self.availability = 0.5
        self.latency = 100.0

        self.score = 0.0
