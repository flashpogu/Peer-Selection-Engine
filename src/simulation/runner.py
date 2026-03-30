import time
from src.scheduler.choke_scheduler import schedule_peers
from src.simulation.environment import update_peer_metrics
from src.utils.logger import SwarmLogger


def run_simulation(peers, weights, upload_slots, steps=10, interval=1):
    logger = SwarmLogger("data/raw/swarm_logs.csv")

    for step in range(steps):
        print(f"\n===== TIME STEP {step + 1} =====")

        update_peer_metrics(peers)

        unchoked = schedule_peers(peers, weights, upload_slots)

        print("Unchoked peers:")
        for peer in unchoked:
            print(peer)

        # 🔹 Log all peers
        for peer in peers:
            logger.log_peer(step + 1, peer)

        time.sleep(interval)
