from src.simulation.peer_generator import generate_peers
from src.simulation.runner import run_simulation


WEIGHTS = {
    "upload": 0.4,
    "reliability": 0.3,
    "availability": 0.2,
    "latency": 0.1
}

UPLOAD_SLOTS = 4
NUM_PEERS = 20
SIMULATION_STEPS = 10


def main():
    peers = generate_peers(NUM_PEERS)

    run_simulation(
        peers=peers,
        weights=WEIGHTS,
        upload_slots=UPLOAD_SLOTS,
        steps=SIMULATION_STEPS,
        interval=1
    )


if __name__ == "__main__":
    main()
