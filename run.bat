@echo off
echo 🚀 Starting AI P2P System...

set "TRACKER_IP=127.0.0.1"

echo 📡 Starting Tracker...
start cmd /k "python tracker/tracker.py"

timeout /t 2 > nul

echo 📊 Starting Monitor...
start cmd /k "set TRACKER_IP=%TRACKER_IP%&& python monitor.py"

echo 🧑‍💻 Starting Peer 1...
start cmd /k "set TRACKER_IP=%TRACKER_IP%&& python -m peer.peer --peer_id peer1 --port 9001"

echo 🧑‍💻 Starting Peer 2...
start cmd /k "set TRACKER_IP=%TRACKER_IP%&& python -m peer.peer --peer_id peer2 --port 9002"

echo 🧑‍💻 Starting Peer 3...
start cmd /k "set TRACKER_IP=%TRACKER_IP%&& python -m peer.peer --peer_id peer3 --port 9003"

timeout /t 3 > nul

echo 📥 Starting Downloader...
start cmd /k "set TRACKER_IP=%TRACKER_IP%&& python -m peer.downloader --peer_id peer2"

echo ✅ System started!
pause