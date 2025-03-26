import os
import subprocess
from config import Config

def process_video_to_hls(video_path):
    hls_output_dir = Config.HLS_FOLDER
    hls_filename = os.path.splitext(os.path.basename(video_path))[0] + ".m3u8"
    hls_output_path = os.path.join(hls_output_dir, hls_filename)

    os.makedirs(hls_output_dir, exist_ok=True)

    ffmpeg_cmd = f'ffmpeg -i "{video_path}" -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{hls_output_path}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

    return f"/hls/{hls_filename}"
