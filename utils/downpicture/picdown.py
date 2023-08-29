import requests
from lxml import etree
import os
from time import sleep

from tiktok_config import User_Avter_Dir

headers = {
    'user - agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.116Safari / 537.36'
}

data_path = User_Avter_Dir
if not os.path.exists(data_path):
    os.mkdir(data_path)


# 得到进一步的页面链接
def get_first_url(url):
    response = requests.get(url=url, headers=headers).text
    html = etree.HTML(response)
    lists = html.xpath('//*[@id="main"]/div[3]/ul')
    for i in range(len(lists)):
        li = lists[i].xpath('./li/a/@href')
    return li


# 得到图片的内容和名称
def get_image_data(url):
    response = requests.get(url=url, headers=headers).text
    html = etree.HTML(response)
    src = html.xpath('//*[@id="img"]/img/@src')[0]
    image_src = 'http://pic.netbian.com' + src  # 得到图片下载地址
    image_data = requests.get(url=image_src, headers=headers).content  # 拿到图片内容
    return image_data


# 保存图片到本地
def download(path, name: str, data):
    save_path = os.path.join(path, name)
    with open(save_path, 'wb') as f:
        f.write(data)
        print(save_path, '=========>下载成功啦！！')
        f.close()


# 获取本次图片爬取的其实index
def return_the_last_index():
    import glob
    user_avter_files = glob.glob(os.path.join(User_Avter_Dir, '*.jpg')) + \
                       glob.glob(os.path.join(User_Avter_Dir, '*.png'))
    if len(user_avter_files) > 0:
        user_avter_files = sorted(user_avter_files, key=lambda name: int(name.split('\\')[-1][:-4]))
        return int(user_avter_files[-1].split('\\')[-1][:-4])
    return 0


def pic_download():
    base_url = 'http://pic.netbian.com/4kmeinv/index_3.html'
    first_url = get_first_url(base_url)
    start_index = return_the_last_index() + 1
    for i in range(len(first_url)):
        print('第{}张正在下载请稍后'.format(i + 1))
        image_url = 'http://pic.netbian.com' + first_url[i]
        name = '%s.jpg' % (start_index + i)
        image_data = get_image_data(image_url)
        download(data_path, name, image_data)
        sleep(1)  # 延迟1秒

