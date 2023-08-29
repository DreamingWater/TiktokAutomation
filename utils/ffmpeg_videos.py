# Lenovo-"Xie Yan"
import glob
import subprocess
import os
import datetime
from moviepy.editor import *
import hashlib
import base64

from tiktok_config import Main_Video_Folder, video_Out_folder, \
    video_time_index_info, video_file_name_copy, Created_mp4

# video_folder = r"F:\VideosCache\MakingDirs\InputVideos\Mainvideos"  # 目标文件夹
# video_Out_folder = os.path.join(video_folder, "Out")  # 输出文件夹
# video_time_index_info = os.path.join(video_folder, "video_info.txt")  # 存储视频time等，用于ffmpeg的视频分割
# video_file_name_copy = os.path.join(video_folder, 'file.txt')  # ffmpeg的视频合成，根据相应的格式书写

composite_file = os.path.join(video_Out_folder, 'output.mp4')  # 合成的视频


# 对视频进行重命名，根据index
def rename_based_index():
    # 设置 mp4 所在目录
    mp4_folder = Main_Video_Folder
    # 遍历 mp4 所在目录，对每个 mp4 文件进行重命名
    for i, file_name in enumerate(os.listdir(mp4_folder)):
        if file_name.endswith(".mp4"):
            old_path = os.path.join(mp4_folder, file_name)
            new_name = f"down_{i}"
            # new_name = new_name.encode('utf-8')
            # bs64_name = base64.b64encode(new_name)
            # bs64_name = bs64_name.decode('utf-8')[:16]
            # new_path = os.path.join(mp4_folder, "%s.mp4"%bs64_name)
            new_path = os.path.join(mp4_folder, "%s.mp4" % new_name)
            os.rename(old_path, new_path)


def composite_videos(ffmpeg_not_needed: object = False) -> object:
    # 读取目录下所有mp4文件
    video_files = []
    for file_name in os.listdir(Main_Video_Folder):
        if file_name.endswith(".mp4"):
            video_files.append(os.path.join(Main_Video_Folder, file_name))
    video_files.sort()

    # 获取每个视频的时长信息和视频名称

    with open(video_time_index_info, "w") as f:
        for video_file in video_files:
            command = ["ffprobe", "-i", video_file, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            duration = stdout.strip().decode() or None
            video_name = os.path.basename(video_file)
            f.write(f"{video_name}: {duration}\n")
    if ffmpeg_not_needed:
        return video_files
    # 将所有时评的文件名按照格式写入文本，方便ffmpeg处理

    with open(video_file_name_copy, "w") as f:
        for video_file in video_files:
            line = f"file '{os.path.join(Main_Video_Folder, video_file)}'\n"
            f.write(line)

    # 拼接所有视频为一个mp4文件
    command = f"ffmpeg -f concat -safe 0 -i {video_file_name_copy} -c copy -y {composite_file}"
    print(command)
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('composite one video successfully')
    return None


def seconds_to_time(seconds):
    """将秒转化为时分秒格式，并返回字符串"""
    delta = datetime.timedelta(seconds=seconds)
    return str(delta)


def split_video(): # 根据 txt中存储的视频时长来实现视频的分割，还原为单个视频
    # 读取 txt 文件中的视频信息
    with open(video_time_index_info, "r") as f:
        video_info = [line.rstrip("\n") for line in f]
    start_time = 0.0
    # 遍历视频信息，对每个视频进行切割
    for i, info in enumerate(video_info):
        video_name, duration = info.split(": ")
        this_video_duration_s = float(duration)  # 视频时长
        output_file = os.path.join(video_Out_folder, f"{i + 1}_{video_name}")
        end_time = start_time + this_video_duration_s
        ffmpeg_cmd = f"ffmpeg -i {Created_mp4} -ss {seconds_to_time(start_time)} -to {seconds_to_time(end_time)} " \
                     f"-c:v libx264 -c:a aac -strict -2 -y {output_file}"
        start_time += this_video_duration_s
        try:  # 执行 FFmpeg 命令
            subprocess.check_call(ffmpeg_cmd)
        except subprocess.CalledProcessError:
            print("An error occurred while running FFmpeg.")


def from_video_to_audio(): # 提取视频的音频
    video = VideoFileClip(composite_file)
    audio = video.audio
    audio.write_audiofile(os.path.join(Main_Video_Folder, 'test.mp3'))
    print(os.path.join(Main_Video_Folder, 'test.mp3'))


def remove_first_frame(input_video=composite_file):  # 移除目标目录下所有视频的第一帧，并保存到输出文件夹下
    output_dir = os.path.dirname(input_video)
    output_video = os.path.join(output_dir, 'out_without_first_frame.mp4')
    # Use FFmpeg to remove first frame from input video and save output video
    os.system(
        f'ffmpeg -r 30 -i "{input_video}" -vf "trim=start_frame=1" -vsync vfr -c:a copy -y "{output_video}"')


def remove_first_frame_dir(input_dir):  # 移除目标目录下所有视频的第一帧，并保存到输出文件夹下
    output_dir = os.path.join(input_dir, 'Remove_first')
    if os.path.exists(output_dir):  # 确保输出文件夹存在，同时清空里面的内容
        def clean_dir(dir_path):
            _files = glob.glob(os.path.join(dir_path, '*'))
            for file in _files:
                if not os.path.isdir(file):
                    os.remove(file)
                else:
                    clean_dir(file)

        clean_dir(output_dir)
    else:
        os.makedirs(output_dir)

    # Iterate over all files in input directory
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            # Check if file is a video file and its frame rate is 30 fps or 50 fps
            if file_path.lower().endswith('.mp4') or file_path.lower().endswith('.avi') or file_path.lower().endswith(
                    '.mov'):
                # Construct output file path
                output_file_path = os.path.join(output_dir, filename)
                # Use FFmpeg to remove first frame from input video and save output video
                os.system(
                    f'ffmpeg -i "{file_path}" -vf "select=gte(n\,1)" -vsync vfr -c:a copy -y "{output_file_path}"')


# 掐头
def cut_the_first_video(input_directory):
    output_directory = os.path.join(input_directory, 'out')

    # 定义一个函数来提取视频
    def extract_video(input_file, output_file):
        # 检查文件名是否包含空格或特殊字符，并用引号引用文件名
        command = f"ffmpeg -i {input_file} " \
                  f"  -y {output_file}"
        try:  # 执行 FFmpeg 命令
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print("An error occurred while running FFmpeg.")

    # 遍历文件夹中的所有视频文件，并进行处理
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            # 检查文件扩展名是否为 .mp4
            if file.endswith(".mp4"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_directory, file)
                extract_video(input_path, output_path)


# 计算视频的总帧数
def calculate_video_num():
    import subprocess
    input_video = r"F:\VideosCache\MakingDirs\InputVideos\Mainvideos\Out\Remove_first\output.mp4"
    # Execute FFprobe command to get total number of frames
    ffprobe_command = ['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0', '-show_entries',
                       'stream=nb_frames', input_video]
    output = subprocess.check_output(ffprobe_command, shell=True)
    num_frames = int(output.decode('utf-8').strip())
    print(num_frames)


# 查看视频每秒的帧率
def check_frame_velocity():
    import subprocess
    # 设置命令
    mp4_file = r"F:\VideosCache\MakingDirs\InputVideos\Mainvideos\Out\Remove_first\output.mp4"
    command = ['ffprobe', '-select_streams', 'v', '-show_streams', mp4_file]
    # 运行命令并获取输出结果
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 解析输出结果获取帧率信息
    for line in result.stdout.decode('utf-8').split('\n'):
        if 'r_frame_rate' in line:
            fps = int(line.split('=')[1].split('/')[0])
            print(f'视频帧率为：{fps}fps')





def composite_videos_order_by_num():
    # 读取目录下所有mp4文件
    video_files = []
    for file_name in os.listdir(Main_Video_Folder):
        if file_name.endswith(".mp4"):
            video_files.append(os.path.join(Main_Video_Folder, file_name))
    video_files = sorted(video_files, key=lambda name: float(name.split('\\')[-1][5:-4]))
    # 获取每个视频的时长信息和视频名称

    with open(video_time_index_info, "w") as f:
        for video_file in video_files:
            command = ["ffprobe", "-i", video_file, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
            result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            duration = stdout.strip().decode() or None
            video_name = os.path.basename(video_file)
            f.write(f"{video_name}: {duration}\n")

    # 将所有时评的文件名按照格式写入文本，方便ffmpeg处理

    with open(video_file_name_copy, "w") as f:
        for video_file in video_files:
            line = f"file '{os.path.join(Main_Video_Folder, video_file)}'\n"
            f.write(line)

    print('composite one video successfully')
