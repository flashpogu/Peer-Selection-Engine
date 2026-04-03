import socket
import os


def get_default_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


TRACKER_IP = os.getenv("TRACKER_IP", get_default_ip())
TRACKER_PORT = 8000

TRACKER_URL = f"http://{TRACKER_IP}:{TRACKER_PORT}"
