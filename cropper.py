import os

import numpy as np
from PIL import Image


def crop_white_box_with_text(image_path):
    # Load image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Convert to grayscale
    gray_img = img.convert("L")
    gray_array = np.array(gray_img)

    # Threshold the image to segment white regions
    threshold = 200  # Adjust this threshold based on your images
    binary_img = np.where(gray_array > threshold, 255, 0).astype(np.uint8)

    # Find bounding box of white region
    white_pixels = np.argwhere(binary_img == 255)
    (min_y, min_x), (max_y, max_x) = white_pixels.min(0), white_pixels.max(0)

    # Crop image to bounding box
    cropped_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))
    # Save cropped image to disk
    out_path = image_path.replace("key_frame", "cropped_frame")
    cropped_img.save(out_path)
    return cropped_img


# Example usage
folder_path = "extracted_frames"
files = sorted(
    [f for f in os.listdir(folder_path) if f.endswith(("png", "jpg", "jpeg"))]
)
for file in files:
    cropped_image_with_text = crop_white_box_with_text(os.path.join(folder_path, file))
