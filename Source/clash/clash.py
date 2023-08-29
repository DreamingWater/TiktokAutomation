# Lenovo-"Xie Yan"
import json
import multiprocessing
import os
import subprocess
import time

import psutil
import pyautogui
import win32con
import yaml

from tiktok_config import Clash_Exe_Path, Clash_Config_List_Yml, Clash_Proxies_Yaml
from loguru import logger

# 定义要启动的程序路径和名称
program_name = "Clash for Windows.exe"  # 定义要关闭的程序名称


def shutdown_clash():
    for proc in psutil.process_iter():
        try:
            # 获取进程的PID、名称、占用内存、当前状态等信息
            process_name = proc.name()
            process_pid = proc.pid
            # 如果进程名称中包含“Excel”字样，则关闭该进程
            if "CLASH" in process_name.upper():
                proc.kill()
                # print(f"{process_name}(PID:{process_pid}) 已被停止")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if not check_clash_state():
        logger.info('Clash is shutdown')
    else:
        logger.error('The Clash shutdown error...')


def check_clash_state():
    program_launched = False
    for process in psutil.process_iter():
        if program_name.lower() in process.name().lower():
            program_launched = True
            break
    return program_launched


# 启动clash程序
def start_clash_exe():
    import subprocess
    process = None
    process = subprocess.Popen([Clash_Exe_Path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # wait for the program to start and config
    if check_clash_state():
        logger.info('The Clash begin to run...')
    else:
        logger.error('The Clash start error...')
        process.kill()


def parse_yaml_file(file_path=Clash_Proxies_Yaml):
    if not os.path.exists(file_path):
        logger.error('Please change the list.yam and the config yaml file')
    yamlConf = None
    with open(file_path, mode="r", encoding="utf-8") as f:
        yamlConf = yaml.load(f.read(), Loader=yaml.FullLoader)

    # 从文件中解析出代理名称
    def get_proxy_name(yamlConf) -> list:
        name_list = []
        for proxies in yamlConf['proxies']:
            name_list.append(proxies['name'])
        return name_list

    return get_proxy_name(yamlConf)


# def set_clash_proxy(file_path:str,proxy_name:str):
# 修改clash的配置文件，实现代理的配置文件改变
def set_clash_proxy(global_setting_name):
    Clash_Yml_Conf = None
    with open(Clash_Config_List_Yml, mode="r", encoding="utf-8") as f:
        Clash_Yml_Conf = yaml.load(f.read(), Loader=yaml.FullLoader)

    Clash_Yml_Conf = change_the_global_setting(Clash_Yml_Conf, global_setting_name)
    Clash_Config_List_Yml1 = Clash_Config_List_Yml
    with open(Clash_Config_List_Yml1, mode="w", encoding="utf-8") as f:
        Clash_Yml_Conf = json.dumps(Clash_Yml_Conf, ensure_ascii=False)

        f.write(Clash_Yml_Conf)


def change_the_global_setting(yml_conf: dict, gloal_setting_name):
    # yaml_setting
    yml_conf['files'][0]['time'] = yml_conf['files'][0]['time']
    # global setting
    yml_conf['files'][0]['selected'][0]['now'] = gloal_setting_name
    return yml_conf
