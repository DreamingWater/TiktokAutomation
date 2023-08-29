# Lenovo-"Xie Yan"
import time, os, requests, json, random, bs4
from rich.text import Text as tekz
from rich.panel import Panel as nel
from rich.panel import Panel
from rich.console import Console
import requests
from lxml import etree

from tiktok_config import Main_Video_Folder


def logo():
    ban = """[green]by Xie Yan
╔═╗╔╗╔╔═╗╔═╗╔╦╗╦╦╔═  
╚═╗║║║╠═╣╠═╝ ║ ║╠╩╗  
╚═╝╝╚╝╩ ╩╩   ╩ ╩╩ ╩ """
    Console(width=50).print(Panel(ban, style='bold black'), justify='center')
    lol = """[white] Masukkan link url post tiktok yang ingin kamu dwonload!!!"""
    Console(width=50).print(Panel(lol, style='bold black'), justify='center')


# 对文件名进行加密，base64编码
def rename_video_base64(_name):
    import base64
    _name = _name.encode('utf-8')
    bs64_name = base64.b64encode(_name)
    bs64_name = bs64_name.decode('utf-8')[:16]
    return bs64_name


class Snaptk_Process:
    def __init__(self):
        self.Session = requests.Session()

    def down_tiktok_video(self, tk_vid, id_vid, at_vid):
        # at_vid 作者名， id_vid 视频的id， tk_vid 视频的token值
        name_vid = rename_video_base64(at_vid + id_vid)
        name_vid = os.path.join(Main_Video_Folder, name_vid)  # 视频保存的位置
        run = self.Session.get(f'https://tikmate.app/download/{tk_vid}/{id_vid}.mp4?hd=1').content
        with open(name_vid, "wb") as sv:
            sv.write(run)
        return True

    # 通过snaptk网页对url进行解析，得到视频的token
    def parse_video_data(self, url):
        data = {"url": url}
        try:
            data = requests.post('https://api.tikmate.app/api/lookup', data=data).text
            resp = json.loads(data)
            if resp['success']:
                tk_vid = resp['token']
                id_vid = resp['id']
                at_vid = resp['author_name']
                self.down_tiktok_video(tk_vid, id_vid, at_vid)  # 下载视频
        except Exception as e:
            print(e)

    def mulai(self):
        # 下载某单个视频
        url = "https://www.tiktok.com/@user1954787057193/video/7227160405515308290"
        self.parse_video_data(url)

    def get_videos_url_from_intr(self, into_url: str):
        # 获取某个用户下面的视频数量
        into_url = "https://www.tiktok.com/@user1954787057193"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        response = requests.get(url=into_url, headers=headers)
        response.encoding = 'UTF-8'
        # 解析响应
        html = etree.HTML(response.text)
        video_data_set = html.xpath('.//div[@data-e2e="user-post-item-list"]/Child')  # video data 组件集合
        print(len(video_data_set))

    def request_object_intr(self):
        # 获取某个用户intr的视频数量
        server_url = 'http://45.14.64.169:3001/return'
        data = {'intr_url': "https://www.tiktok.com/@musingxer"}
        response = requests.post(url=server_url, data=data)
        response.encoding = 'UTF-8'
        # 解析响应
        html = etree.HTML(response.text)
        video_url = html.xpath('.//div[@data-e2e="user-post-item"]//a/@href')
        print(len(video_url))



# Snaptk_Process().get_videos_url_from_intr('a')
Snaptk_Process().request_object_intr()
