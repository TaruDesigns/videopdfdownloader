import os

from PIL import Image

folder_path = "extracted_frames"

imagelist = sorted(
    [
        f
        for f in os.listdir(folder_path)
        if (f.endswith(("png", "jpg", "jpeg")) and f.startswith("cropped_frame"))
    ]
)

images = [Image.open(os.path.join(folder_path, f)) for f in imagelist]

os.makedirs("output", exist_ok=True)
pdf_path = "./output/out.pdf"

images[0].save(
    pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
)
