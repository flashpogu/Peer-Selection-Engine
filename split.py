# tools/split_file.py
import os
CHUNK_SIZE = 256 * 1024  # 256 KB

input_file = "video.mp4"
output_dir = "peer/shared/chunks"

os.makedirs(output_dir, exist_ok=True)

with open(input_file, "rb") as f:
    i = 0
    while True:
        data = f.read(CHUNK_SIZE)
        if not data:
            break
        with open(f"{output_dir}/chunk_{i}", "wb") as out:
            out.write(data)
        i += 1

print(f"Created {i} chunks")
