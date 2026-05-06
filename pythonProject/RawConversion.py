from PIL import Image, ImageOps
import numpy as np

# allow very large images
Image.MAX_IMAGE_PIXELS = None


def convert_map_to_tif(input_path, output_path, compression="tiff_lzw"):
    with Image.open(input_path) as img:
        print(f"Map loaded: {img.mode}, {img.size}")
        img.save(output_path, format="TIFF", compression=compression)
        print(f"Saved map → {output_path}")


def convert_mask_to_tif_inverted(input_path, output_path, compression="tiff_lzw"):
    with Image.open(input_path) as img:
        print(f"Mask loaded: {img.mode}, {img.size}")

        # --- invert safely ---
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            rgb = Image.merge("RGB", (r, g, b))
            inverted_rgb = ImageOps.invert(rgb)
            img = Image.merge("RGBA", (*inverted_rgb.split(), a))
        else:
            img = ImageOps.invert(img)

        img.save(output_path, format="TIFF", compression=compression)
        print(f"Saved inverted mask → {output_path}")

# ===== USAGE =====
convert_map_to_tif("map_raw.png", "map_raw.tif")
convert_mask_to_tif_inverted("mask_raw.png", "mask_raw.tif")