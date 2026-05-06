import os
from PIL import Image

def convert_png_to_tif(input_dir, output_dir=None):
    if output_dir is None:
        output_dir = input_dir + "_tif"

    for root, dirs, files in os.walk(input_dir):
        # recreate folder structure
        rel_path = os.path.relpath(root, input_dir)
        target_root = os.path.join(output_dir, rel_path)
        os.makedirs(target_root, exist_ok=True)

        for file in files:
            if file.lower().endswith(".png"):
                input_path = os.path.join(root, file)
                output_name = os.path.splitext(file)[0] + ".tif"
                output_path = os.path.join(target_root, output_name)

                with Image.open(input_path) as img:
                    img.save(output_path, format="TIFF")

    print(f"Conversion complete → {output_dir}")


# ===== USAGE =====
convert_png_to_tif("output")