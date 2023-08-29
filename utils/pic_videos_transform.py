# Lenovo-"Xie Yan"
import shutil
import subprocess
import os, glob
from tiktok_config import RUBBISHCACHE_DIR, Created_mp4, REINDEX_JPG_DIR, Output_finish, LingFox_video_folder
from utils.common import common_clean_dir


# use ffmpeg to convert videos to jpgs....
def videos_to_jpgs(video_name, frame_number=50):
    videos_file = video_name
    cmd = 'ffmpeg -i {} -r {} -f image2 {}\%05d.jpg'.format(videos_file, frame_number, RUBBISHCACHE_DIR)
    subproc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 等待进程执行结束
    out, err = subproc.communicate()


# 删除部分帧数
def delete_some_frame(frame_number=30):
    jpgs_files_ = os.path.join(RUBBISHCACHE_DIR, '*.jpg')  # jgps的glob文件匹配名
    jpgs_files = glob.glob(jpgs_files_)
    print('视频提取的图片总数:{}'.format(len(jpgs_files)))
    delete_num = len(jpgs_files) // frame_number  # 需要删除的图片数量
    delete_pics_index = [(frame_number-1) * i for i in range(1, delete_num + 1)]  # 需要删除图片的indexs
    for index in delete_pics_index:
        os.remove(jpgs_files[index])
    print('succeed to delete the setting frame.')
    print('视频抽除之后的图片总数:{}'.format(len(glob.glob(jpgs_files_))))


# 图片帧拼接为视频
def frame_splicing(jpgs_dir=REINDEX_JPG_DIR, out_dir = Output_finish ,
                   target_video_name='output.mp4', frame_number=30):
    target_video = os.path.join(Output_finish, target_video_name)
    jpgs_file = os.path.join(jpgs_dir, '%05d.jpg')
    command = 'ffmpeg -i {} -r {} -y {}'.format(jpgs_file, frame_number, target_video)
    command_vcodec = 'ffmpeg -i {} -vcodec mpeg4 -r {} -y {}'.format(jpgs_file, frame_number, target_video)
    subproc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 等待进程执行结束
    out, err = subproc.communicate()


def frame_extraction(clip_, frame_number=30):
    print('视频的帧数为{:.2f}'.format(clip_.fps))
    # clean_dir(RUBBISHCACHE_DIR)
    # videos_to_jpgs(clip_)    # 将视频抽帧为jpgs
    # delete_some_frame()      # 删除部分帧数
    # frame_splicing()  # 实现帧拼接


def regenerate_index(dir_path=RUBBISHCACHE_DIR):
    if not os.path.exists(REINDEX_JPG_DIR):
        os.makedirs(REINDEX_JPG_DIR)
    jpg_png = glob.glob(os.path.join(dir_path, '*.jpg'))
    path = sorted(jpg_png, key=lambda name: float(name.split('\\')[-1][:-4]))
    for index, file in enumerate(path):
        refine_index = index + 1  # 从1开始计算
        shutil.copy(file, os.path.join(REINDEX_JPG_DIR, '%05d.jpg' % refine_index))  # 可以复制到目录下


# frame_extraction(clip)
def video_pic_videos_(video_dir=LingFox_video_folder):
    videos_files = glob.glob(os.path.join(video_dir, '*.mp4'))
    # index = 1
    for video in videos_files:
        common_clean_dir(RUBBISHCACHE_DIR)
        videos_to_jpgs(video, frame_number=30)
        delete_some_frame()
        regenerate_index()
        frame_splicing(target_video_name=video.split('\\')[-1],
                       out_dir=Output_finish)     # 文件存储在 Output_finish 文件夹
        # index += 1
        # if index > 4:
        #     break


# if __name__ == '__main__':
#     main()
