# This is a sample Python script.
import random
import time

from requests.exceptions import ProxyError

from Browser.outlook_login import OutlookMailLogin
from Browser.tk_login import TkLogin
from Browser.user_meta import RandomUserMeta
from Source.clash.clash import shutdown_clash, start_clash_exe
from utils.logging.logging import loguru_config, logger
from Browser.tk_signup import TkSignup
from Jianying.JianYingContainer import jianying_json_change, jianying_create_project, jianying_combine_json, \
    jianying_start_project
from Jianying.JianYingSrt import jianying_srt_export
from Jianying.Scripts.json_parse import get_element_from_json

from tiktok_config import Created_mp4, Combine_mp4, Src_Json_File
from utils.check_ip import judge_internet_connected

from utils.common import get_newest_project, horn_prompt
from utils.ffmpeg_videos import remove_first_frame, composite_videos, split_video, cut_the_first_video, \
    rename_based_index, remove_first_frame_dir, composite_file, calculate_video_num, check_frame_velocity, \
    composite_videos_order_by_num
from utils.pic_videos_transform import video_pic_videos_
from utils.sqlite_db import update_the_tb


def main():
    pass
    # rename_based_index()
    # composite_videos()    # 实现视频的拼接
    # remove_first_frame()  # 移除视频的第一帧
    # calculate_video_num()
    # remove_first_frame_dir(r'F:\VideosCache\MakingDirs\InputVideos\Mainvideos\Out')  # 移除视频的第一帧
    # jianying_create_project()      # jianying 工程创建

    # composite_videos_order_by_num()


def combine_video_process():  # 视频合成进程
    jianying_create_project()  # 创建jianying工程
    project_path = get_newest_project()  # 获取目标工程的目录
    videos_list = composite_videos(True)  # 获取视频文件夹下视频的序列
    jianying_combine_json(project_path, videos_list)  # 利用jianying来合成视频
    jianying_start_project(Combine_mp4)  # 剪映保存视频，名称为combine.mp4''


def duplicate_removal_process():
    jianying_create_project()  # 创建jianying工程
    project_path = get_newest_project()  # 获取目标工程的目录
    jianying_json_change(project_path)  # 通过修改json文件实现剪映的修改
    jianying_start_project(Created_mp4)  # 剪映保存视频，名称为'created.mp4'


def split_video_2_videos():
    from utils.ffmpeg_videos import split_video
    split_video()  # 分割视频


########## 灵狐剪辑 ###########
###  掐头 去尾 ###
###########灵狐结束############

#########视频 >> 图片  >> 视频
def video2pic2video():
    video_pic_videos_()


def tk_into():  # tiktok 主页爬取
    from Browser.tk_introduction import TkIntroduction
    TkIntroduction().get_tk_website()  # .get_comments_info()#


def outlook_register():  # outlook 注册
    from Browser.outlook_register import OutlookMailRegister
    outlook_ = OutlookMailRegister()
    res = outlook_.get_outlook_website()
    if res:
        logger.success('succeed to register one outlook email')


# tk 注册页面
def tk_signup(email, password):
    tk_sign = TkSignup()
    tk_sign.get_signup_website(email, password)


# 获取clash文件的proxies name，然后 注册tiktok
def get_clash_config_name():
    from Source.clash.clash import parse_yaml_file, set_clash_proxy
    from utils.sqlite_db import get_raw_login_info

    IP_LIST = []  # useful ip list
    proxy_names = parse_yaml_file()  # 读取网络配置文件信息
    accounts_infos = get_raw_login_info()  # 从数据库拿email passwd信息
    # proxy_name_set = False
    # proxy_names = proxy_names[::-1]
    for proxy_name in proxy_names:  # 取出一个节点
        if '台湾' in proxy_name: #or '阿根廷' in proxy_name or '美国A' in proxy_name:
            continue
        shutdown_clash()  # 关闭clash
        set_clash_proxy(proxy_name)  # 将节点取出，并设置到配置文件中
        start_clash_exe()  # 启动 clash 程序
        this_ip = judge_internet_connected()  # 检测这个IP
        if this_ip and this_ip not in IP_LIST:  # 如果IP可用,而且之前没有出现过
            # 使用该IP
            logger.success('this IP:{} of name:{} is of use'.format(this_ip, proxy_name))
            # print(accounts_infos[len(IP_LIST)]['email'],accounts_infos[len(IP_LIST)]['password'])
            outlook_register()  # outlook 注册
            # tk_signup(email=accounts_infos[len(IP_LIST)]['email'], password=accounts_infos[len(IP_LIST)]['password'])
            IP_LIST.append(this_ip)  # 放在后面
            # while 1:
            #     print('waiting')
            #     time.sleep(10)
        else:
            # 换下一轮
            logger.warning('the proxy_name:{} is useless...'.format(proxy_name))
            continue


def outlook_email(this_ip):
    outlook_login = OutlookMailLogin()
    outlook_login.login('***@outlook.com', '***')
    result = outlook_login.find_the_tk_email()
    if result:
        logger.critical('succeed to get the website based on ip:{}'.format(this_ip))


if __name__ == '__main__':
    loguru_config()
    # tk 注册
    # tk_signup(email='f1fsdDGDSF232se3wrfeeef' + str(random.randint(1, 100)) + '@outlook.com', password='fsdf3we123@223')
    # outlook_register()
    # while True:
    #     outlook_register()
    # get_clash_config_name()
    # tk_signup('','')
    # tk 登录
    # tk_login = TkLogin()
    # tk_login.get_login_website('***@outlook.com', '***') 
    # tk 页面
    tk_into()
    # outlook 登录
    # outlook_login = OutlookMailLogin()
    # outlook_login.login('***@outlook.com','***')
    # input('wating')
    # user email password save
    # user = RandomUserMeta()
    # user.request_user_meta()
    # user.email, user.password = '***@outlook.com', '***'
    # user.save_user_data()

    # get_clash_config_name()
    # get_clash_config_name()
    # start_clash_exe()
    # get_clash_config_name()
    # test_xpath()
    # combine_video_process()  # 启动视频合成进程
    # check_frame_velocity()
    # jianying_start_project(Combine_mp4)  # 剪映保存视频，名称为combine.mp4''
    # jianying_start_project(Combine_mp4)  # 剪映保存视频，名称为combine.mp4''
    # video_pic_videos_()
    # Lenovo-"Xie Yan"
    # jianying_srt_export()  # 剪影 srt 字幕导出
    # tk_into()
    # test_xpath()

#### tk sign up page
# tk_sign = TkSignup()
# tk_sign.get_signup_website()


###
