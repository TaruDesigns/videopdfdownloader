import logging
import os
import shutil

import numpy as np
from ffmpeg import FFmpeg
from PIL import Image
from yt_dlp import YoutubeDL


def folder_cleanup(video_id: str):
    try:
        shutil.rmtre(os.path.join("./temp", video_id))
    except Exception as e:
        logging.warn(e)
    # os.makedirs(os.path.join("./temp", video_id, "downloads")
    # os.makedirs(os.path.join("./temp", video_id, "frames", "raw")
    # os.makedirs(os.path.join("./temp", video_id, "frames", "processed")
    # os.makedirs(os.path.join("./temp", video_id, "pdf")


def download_youtube_video(url: str = None, output_path="video.mp4") -> dict:
    """Downloads video to disk using yt-dlp

    Args:
        url (str): url of the video
        output_path (str, optional): output path of the video. Defaults to "video.mp4".
    """
    if url is None:
        raise ValueError("URL Cannot be empty")
    # Download best quality
    os.makedirs(os.path.dirname(output_path))
    ydl_opts = {
        "format": "bestvideo",
        "outtmpl": output_path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    logging.info(f"Downloaded video to {output_path}")


def extract_youtube_info_from_url(url: str = None) -> dict:
    """Extracts video info

    Args:
        url (str): youtube video url
    """
    if url is None:
        raise ValueError("URL Cannot be empty")
    # Download best quality
    ydl_opts = {
        "format": "bestvideo",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
    logging.info(f"Extracted video info for {url}")
    return info


def split_video_into_key_frames(
    video_path: str,
    frames_folder: str = "raw",
    start_time: str = None,
    threshold: float = 0.0128,
):
    """Splits video into keyframes (==keep only unique frames, mostly) using ffmpeg

    Args:
        video_path (str): local path in disk
        frames_folder (str, optional): destination of the extracted frames
        start_time (str, optional): start time, used to ignore blank beginning of video
        threshold (float, optional): magic value for ffmpeg to decide how similar a frame is to the next
    """
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    # Use ffmpeg-python to extract only key frames
    ffmpeg = FFmpeg()
    if start_time:  # Start time is a timestamp like 00:00:00
        ffmpeg.input(video_path, ss=start_time)
    else:
        ffmpeg.input(video_path)
    ffmpeg.output(
        os.path.join(frames_folder, "key_frame_%05d.png"),
        vf=f"select=gt(scene\,{threshold})+eq(n\,0)",  # The second filter is just first frame because it wouldn't get it otherwise
        # vf="select=eq(pict_type\\,I)", This one is good for filtering most of the good frames but it has repeats
        vsync="vfr",
    )
    logging.info(f"Extracting frames for video: {video_path}")
    ffmpeg.execute()
    logging.info(f"Extracted key frames to {frames_folder}")
    frames_list = sorted(
        [
            os.path.join(frames_folder, f)
            for f in os.listdir(frames_folder)
            if f.endswith(("png"))
        ]
    )
    return frames_list


"""
def remove_duplicate_images(folder_path, threshold_percentage=0.05):
    # Doesn't actually work, it's old stuff.
    # List all files in the folder and sort them
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(("png", "jpg", "jpeg"))]
    )

    previous_image = None
    previous_image_filepath = ""

    for i, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        current_image = Image.open(file_path)
        current_image_filepath = file_path

        if previous_image is not None:
            # Convert images to numpy arrays for comparison
            np_previous = np.array(previous_image)
            np_current = np.array(current_image)

            # Compute the absolute difference between images
            abs_diff = np.abs(np_previous - np_current)

            # Calculate percentage difference
            percentage_diff = np.sum(abs_diff) / (np_previous.size * 255)
            print(
                f"Previous: {previous_image_filepath}, current: {current_image_filepath}, diff: {percentage_diff}"
            )

            # If the percentage difference is below the threshold, remove the image
            if percentage_diff < threshold_percentage:
                os.remove(file_path)
                print(f"Removed duplicate image: {file}")
            else:
                # Show the difference if it's above the threshold
                # show_difference(previous_image, current_image)
                previous_image = current_image
        else:
            previous_image = current_image
            previous_image_filepath = file_path
"""


def postprocess_images_sheetmusic(frames_list: list[str]):
    postprocessed_images = sorted([postprocess_image(f) for f in frames_list])
    return postprocessed_images

    ...


def postprocess_image(image_path: str = None) -> str:
    """Crops image to remove any black background and leave only the white part (for sheet music)

    Args:
        image_path (str): Image path to be cropped

    Returns:
        str: Output path of the processed image
    """
    # Load image
    if image_path is None:
        raise ValueError("Image path cannot be null")
    output_folder = os.path.join(os.path.dirname(image_path), "processed")
    os.makedirs(output_folder, exist_ok=True)
    img = Image.open(image_path)

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
    out_imgname = image_path.replace("key_frame", "cropped_frame")
    out_path = os.path.join(output_folder, out_imgname)
    cropped_img.save(out_path)
    return out_path


def images_to_pdf(imglist: str = None, output_file: str = "out.pdf"):
    images = [Image.open(f) for f in imglist]

    os.makedirs(os.path.join(os.path.dirname(output_file), exist_ok=True))

    images[0].save(
        output_file, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )


if __name__ == "__main__":
    ...
    url = "https://www.youtube.com/watch?v=SEwqRF-_hsk"
    ytinfo = extract_youtube_info_from_url(url=url)
    folder_cleanup(video_id=ytinfo["id"])
