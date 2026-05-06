import os
import numpy as np
from PIL import Image


def delete_all_black_pairs(root_dir):
    deleted = 0
    checked = 0

    for block_name in sorted(os.listdir(root_dir)):
        block_path = os.path.join(root_dir, block_name)

        if not os.path.isdir(block_path):
            continue

        for fname in sorted(os.listdir(block_path)):
            if not fname.startswith("mask_"):
                continue

            mask_path = os.path.join(block_path, fname)
            map_name = fname.replace("mask_", "map_", 1)
            map_path = os.path.join(block_path, map_name)

            checked += 1

            with Image.open(mask_path) as mask:
                arr = np.array(mask)

            # delete if every pixel is zero
            if not np.any(arr):
                os.remove(mask_path)

                if os.path.exists(map_path):
                    os.remove(map_path)

                deleted += 1
                print(f"Deleted: {map_name} + {fname}")

    print(f"\nChecked {checked} pairs")
    print(f"Deleted {deleted} all-black pairs")


# ===== USAGE =====
delete_all_black_pairs("output_300")