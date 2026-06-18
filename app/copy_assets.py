import os
import shutil

# Target directory
target_dir = r"G:\Antigravity Projects\agy\app\static\images"
os.makedirs(target_dir, exist_ok=True)

# Source images in artifact directory
artifact_dir = r"C:\Users\skixr\.gemini\antigravity-cli\brain\2c94a3e2-368e-4a64-9d14-71572f578969"

mapping = {
    "dune_three_poster_1781819769350.jpg": "dune_three_poster.jpg",
    "spiderman_poster_1781819788464.jpg": "spiderman_poster.jpg",
    "doomsday_poster_1781819798980.jpg": "doomsday_poster.jpg",
    "odyssey_poster_1781819807248.jpg": "odyssey_poster.jpg"
}

for src_name, dest_name in mapping.items():
    src_path = os.path.join(artifact_dir, src_name)
    dest_path = os.path.join(target_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} -> {dest_name}")
    else:
        print(f"Source file not found: {src_path}")
