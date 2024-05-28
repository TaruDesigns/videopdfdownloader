import os

import numpy as np
from ffmpeg import FFmpeg
from PIL import Image, ImageChops
from yt_dlp import YoutubeDL


def download_youtube_video(url, output_path="video.mp4"):
    ydl_opts = {
        "format": "bestvideo",
        "outtmpl": output_path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Downloaded video to {output_path}")


def split_video_into_key_frames(
    video_path, frames_folder="key_frames", start_time=None, threshold=0.0128
):
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    # Use ffmpeg-python to extract only key frames
    ffmpeg = FFmpeg()
    if start_time:
        ffmpeg.input(video_path, ss=start_time)
    else:
        ffmpeg.input(video_path)
    ffmpeg.output(
        os.path.join(frames_folder, "key_frame_%05d.png"),
        vf=f"select=gt(scene\,{threshold})+eq(n\,0)",  # The second filter is just first frame because it wouldn't get it otherwise
        # vf="select=eq(pict_type\\,I)", This one is good for filtering most of the good frames but it has repeats
        vsync="vfr",
    )
    ffmpeg.execute()
    print(f"Extracted key frames to {frames_folder}")


def remove_duplicate_images(folder_path, threshold_percentage=0.05):
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


url = "https://www.youtube.com/watch?v=SEwqRF-_hsk"
try:
    video_id = url.split("watch?v=")[1]
except Exception as e:
    raise ("Video ID was not found")
video_path = "downloaded_video.mp4"
frames_folder = "extracted_frames"

download_youtube_video(url, video_path)
split_video_into_key_frames(video_path, frames_folder)
