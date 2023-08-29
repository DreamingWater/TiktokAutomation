# Lenovo-"Xie Yan"
import subprocess

from moviepy.video.io.VideoFileClip import VideoFileClip


# 获取视频的时长 us
def get_video_duration(video_file):
    # video = VideoFileClip(video_path)
    # duration = video.duration
    # duration_us = int(duration * 1000 * 1000)
    # return duration_us
    command = ["ffprobe", "-i", video_file, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()
    duration = stdout.strip().decode() or None
    if duration is None:
        return -1
    duration = float(duration)
    return duration * 10 ** 6
