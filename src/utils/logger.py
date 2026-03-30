import csv
import os


class SwarmLogger:
    def __init__(self, filepath):
        self.filepath = filepath
        self._init_file()

    def _init_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestep",
                "peer_id",
                "upload_rate",
                "reliability",
                "availability",
                "latency",
                "score",
                "choked",
                "selected"
            ])

    def log_peer(self, timestep, peer):
        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestep,
                peer.peer_id,
                round(peer.upload_rate, 2),
                round(peer.reliability, 2),
                round(peer.availability, 2),
                round(peer.latency, 2),
                round(peer.score, 2),
                peer.choked,
                not peer.choked
            ])
