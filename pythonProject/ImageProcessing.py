import os
from PIL import Image
from PIL import ImageOps
import math

Image.MAX_IMAGE_PIXELS = 1_000_000_000  # 1 billion

def split_into_blocks(img, n_blocks):

    width, height = img.size

    cols = math.ceil(math.sqrt(n_blocks))
    rows = math.ceil(n_blocks / cols)

    block_w = width // cols
    block_h = height // rows

    blocks = []

    for r in range(rows):
        for c in range(cols):
            left = c * block_w
            upper = r * block_h

            right = (c + 1) * block_w if c < cols - 1 else width
            lower = (r + 1) * block_h if r < rows - 1 else height

            block = img.crop((left, upper, right, lower))
            blocks.append(block)

            if len(blocks) >= n_blocks:
                return blocks

    return blocks


def tile_block(img, tile_size, overlap):
    tiles = []
    w, h = img.size

    stride = tile_size - overlap
    assert stride > 0, "Overlap must be smaller than tile size!"

    for y in range(0, h - tile_size + 1, stride):
        for x in range(0, w - tile_size + 1, stride):
            tile = img.crop((x, y, x + tile_size, y + tile_size))
            tiles.append(tile)

    return tiles


def process(map_path, mask_path, output_dir, n_blocks=10, tile_size=80, overlap=20):
    map_img = Image.open(map_path)
    mask_img = Image.open(mask_path)

    assert map_img.size == mask_img.size, "Map and mask must match size!"

    map_blocks = split_into_blocks(map_img, n_blocks)
    mask_blocks = split_into_blocks(mask_img, n_blocks)

    os.makedirs(output_dir, exist_ok=True)

    for i, (m_block, mk_block) in enumerate(zip(map_blocks, mask_blocks), start=1):
        block_folder = os.path.join(output_dir, f"block_{i:02d}")
        os.makedirs(block_folder, exist_ok=True)

        map_tiles = tile_block(m_block, tile_size, overlap)
        mask_tiles = tile_block(mk_block, tile_size, overlap)

        for j, (mt, mkt) in enumerate(zip(map_tiles, mask_tiles), start=1):
            map_name = f"map_block{i:02d}_tile{j:05d}.png"
            mask_name = f"mask_block{i:02d}_tile{j:05d}.png"

            # --- invert mask safely ---
            if mkt.mode == "RGBA":
                r, g, b, a = mkt.split()
                rgb = Image.merge("RGB", (r, g, b))
                inverted_rgb = ImageOps.invert(rgb)
                mkt = Image.merge("RGBA", (*inverted_rgb.split(), a))
            else:
                mkt = ImageOps.invert(mkt)

            mt.save(os.path.join(block_folder, map_name))
            mkt.save(os.path.join(block_folder, mask_name))


# ===== USAGE =====
process(
    map_path="map_raw.png",
    mask_path="mask_raw.png",
    output_dir="output_300",
    n_blocks=10,
    tile_size=300,
    overlap=20   # <-- adjust this
)