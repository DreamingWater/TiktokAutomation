# Lenovo-"Xie Yan"
import glob
import msvcrt
import os
import sys
import time
import threading
import time
import winsound

from tiktok_config import Verication_Tk_Dir


def get_newest_project(draft_dir=r"D:\ProgramFiles\VideoDesign\Jianying\JianyingPro Drafts"):  # 获取最新的工程
    import os
    dir_list = os.listdir(draft_dir)  # draft 工程文件夹
    sorted_dir = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(draft_dir, x)), reverse=True)
    return os.path.join(draft_dir, sorted_dir[0])


def common_clean_dir(dir_path):  # 清理文件夹的所有文件，但是不清理子文件夹
    files = glob.glob(os.path.join(dir_path, '*'))
    for file in files:
        if not os.path.isdir(file):
            os.remove(file)
        else:
            common_clean_dir(file)


# 喇叭提示
def horn_prompt():
    winsound.Beep(2222, 111)

    # 定义一个子线程来等待键盘输入
    def input_thread():
        input('please input sth and then deal the verication')

    t = threading.Thread(target=input_thread)
    t.daemon = True
    t.start()
    # 每隔1秒钟播放提示音，检查子线程状态结束循环
    while t.is_alive():
        winsound.MessageBeep()
        time.sleep(1)


import os
import requests


def common_download_image(url, filename, Outdir=Verication_Tk_Dir):
    """下载图片并保存到指定目录
    :param url: 图片 URL
    :param outdir: 保存图片的目标目录
    """
    if not filename.endswith('.png'): #  确保有后缀名
        filename = "%s.png" % filename
    # 从 URL 中获取文件名
    filepath = os.path.join(Outdir, filename)
    proxies = {
        'http': f'socks5h://127.0.0.1:7890',
        'https': f'socks5h://127.0.0.1:7890',
    }
    # 设置环境变量
    os.environ['HTTP_PROXY'] = proxies['http']
    os.environ['HTTPS_PROXY'] = proxies['https']

    # 使用 requests 库发送请求
    response = requests.get(url, proxies=proxies)
    # 将图片保存到本地文件
    with open(filepath, 'wb') as f:
        f.write(response.content)
    print(filepath)


def judge_one_not_in_list():
    pass