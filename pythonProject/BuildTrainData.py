import os
import random
import numpy as np
from PIL import Image


def collect_block_pairs(root_dir):
    block_pairs = {}

    for block_name in sorted(os.listdir(root_dir)):
        block_path = os.path.join(root_dir, block_name)
        if not os.path.isdir(block_path):
            continue

        maps = {}
        masks = {}

        for fname in sorted(os.listdir(block_path)):
            if fname.startswith("map_"):
                key = fname.replace("map_", "")
                maps[key] = os.path.join(block_path, fname)

            elif fname.startswith("mask_"):
                key = fname.replace("mask_", "")
                masks[key] = os.path.join(block_path, fname)

        common = sorted(set(maps.keys()) & set(masks.keys()))

        pairs = [(maps[k], masks[k]) for k in common]

        if pairs:
            block_pairs[block_name] = pairs

    return block_pairs


def load_pairs(pair_list):
    map_arr = []
    mask_arr = []

    for map_path, mask_path in pair_list:
        with Image.open(map_path) as m:
            map_arr.append(np.array(m))

        with Image.open(mask_path) as mk:
            mask_arr.append(np.array(mk))

    return np.stack(map_arr), np.stack(mask_arr)


def build_train_test(
    root_dir,
    output_dir="npy_output",
    train_ratio=0.8,
    seed=42
):
    os.makedirs(output_dir, exist_ok=True)

    block_pairs = collect_block_pairs(root_dir)

    block_names = sorted(block_pairs.keys())

    random.seed(seed)
    random.shuffle(block_names)

    n_train = max(1, int(len(block_names) * train_ratio))

    train_blocks = block_names[:n_train]
    test_blocks = block_names[n_train:]

    train_pairs = []
    test_pairs = []

    for b in train_blocks:
        train_pairs.extend(block_pairs[b])

    for b in test_blocks:
        test_pairs.extend(block_pairs[b])

    train_map, train_mask = load_pairs(train_pairs)
    test_map, test_mask = load_pairs(test_pairs)

    np.save(os.path.join(output_dir, "train_map.npy"), train_map)
    np.save(os.path.join(output_dir, "train_mask.npy"), train_mask)
    np.save(os.path.join(output_dir, "test_map.npy"), test_map)
    np.save(os.path.join(output_dir, "test_mask.npy"), test_mask)

    print("Done.")
    print(f"Train blocks: {train_blocks}")
    print(f"Test blocks: {test_blocks}")
    print(f"train_map shape: {train_map.shape}")
    print(f"train_mask shape: {train_mask.shape}")
    print(f"test_map shape: {test_map.shape}")
    print(f"test_mask shape: {test_mask.shape}")


# ===== USAGE =====
build_train_test("output_300")