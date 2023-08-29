import json

from Jianying import JianYingApi
from Jianying.JianYingApi.Effect_deal import *
from Jianying.JianYingApi.Videos_deal import *
from tiktok_config import JianYing_Export_Dir, JianYing_Exe_Path, Content_Json_File


class JianYingContainer:
    def __init__(self, Project_Dir):
        self.videos = []  # 视频元素集合
        self.effect_filer = []  # 视频滤镜集合
        self.special_effect = []  # 视频特效集合
        self.duration = None
        self.main_video = None
        self.draft = JianYingApi.Drafts.Create_New_Drafts(Project_Dir)  # Create New Project

    def add_video(self, video_element, duration_need=False):
        if duration_need:
            self.main_video = video_element
        self.videos.append(video_element)

    def video_handle(self, video_path, video_index, alpha=1.0, scale=None, rotation=0.0, transform=None,
                     video_effects=None, flip=None, source_start=None, new_track=True):
        effect_uuid = []  # effect uuid 如果视频具有effect才需要
        if video_effects is not None and type(video_effects) == list:  # 如果视频有特效 滤镜效果
            for _video_effect in video_effects:
                self.draft, _effect_uuid = EffectElement(draft=self.draft).add_one_effect(_video_effect,
                                                                                          effect_type='effect_video')  # 将effect的material添加到draft
                effect_uuid.append(_effect_uuid)  # 将视频特效的material的id保存，后面一起导入
        return VideoElement(draft=self.draft, video_path=video_path) \
            .add_one_video(main_video_duration=self.duration, render_index=video_index, source_start=source_start,
                           alpha=alpha, scale=scale, rotation=rotation, transform=transform, extra_material=effect_uuid
                           , flip=flip, new_track=new_track)

    def parse_video(self):  # add video file to jianying
        for video_index, video in enumerate(self.videos):
            if self.duration is None:  # main video ,the duration is base on it
                self.draft, self.duration = self.video_handle(video_index=video_index, **video)
            else:
                self.draft, _ = self.video_handle(video_index=video_index, **video)

    def add_effect_filter(self, _effect):
        self.effect_filer.append(_effect)

    def add_effect_video(self, _effect):
        self.special_effect.append(_effect)

    def parse_effect(self, effect_type='effect_filter'):  # add effects to jianying
        (base_index, effects) = (10000, self.effect_filer) if effect_type == 'effect_filter' else (
            11000, self.special_effect)  # index 和 effetc列表的获取
        for effect_index, effect in enumerate(effects):
            effect_index_render = base_index + effect_index
            self.draft, _ = EffectElement(draft=self.draft).add_one_effect(effect_type=effect_type,
                                                                           duration=self.duration, render_index=
                                                                           effect_index_render, **effect)

    def parse_config_json(self):
        # 读取json文件
        with open(Content_Json_File, encoding='utf-8') as f:
            data = json.load(f)
        self.videos = []  # 将读取的json数据存储到list
        # 解析 video
        for _video in data['videos']:
            self.videos.append(_video)
        # 解析 effect_filter
        for _effect_filer in data['effects']:
            self.effect_filer.append(_effect_filer)
        # 解析 special_effect
        for _special_effect in data['video_effects']:
            self.special_effect.append(_special_effect)

    def combine_videos(self, videos_path_list):
        for video_index, video_path in enumerate(videos_path_list):
            effect = {"source_start": 0, "new_track": True} if video_index == 0 else {"source_start": 0,
                                                                                      "new_track": False}
            self.draft, _ = self.video_handle(video_index=video_index, video_path=video_path, **effect)


def jianying_json_change(Project_Dir):
    my_jy_element = JianYingContainer(Project_Dir)
    # 从config文件中获得配置信息
    my_jy_element.parse_config_json()
    #######################################  video 视频      #######################################
    my_jy_element.parse_video()

    #######################################  Effects 视频      #######################################
    my_jy_element.parse_effect()  # filter
    my_jy_element.parse_effect(effect_type='specialeffect')  # effect_video

    # 保存
    my_jy_element.draft.Save()


# 创建一个剪影工程
def jianying_create_project():
    _ins = JianYingApi.Jy_Warp.Instance(Start_Jy=True,
                                        JianYing_Exe_Path=JianYing_Exe_Path)
    JianYingApi.Logic_warp.echo("Creat Main Instance.")
    while JianYingApi.Logic_warp._has_running() == False: JianYingApi.Logic_warp.lag()
    _ins._Start_New_Draft_Content(wait=True)  # 进入主页面
    _ins._Close()


# 启动一个草稿工程
def jianying_start_project(export_file: str):
    _ins = JianYingApi.Jy_Warp.Instance(Start_Jy=True,
                                        JianYing_Exe_Path=JianYing_Exe_Path)
    JianYingApi.Logic_warp.echo("Creat Main Instance.")
    while JianYingApi.Logic_warp._has_running() == False: JianYingApi.Logic_warp.lag()
    _ins._Select_Drafts(0)  # 选择第一个草稿并进入主界面
    export_name = export_file.split('\\')[-1][:-4]  # 根据文件路径获取文件名
    Export_Options = JianYingApi.Jy_Warp.Export_Options(
        export_vid=True,
        export_name=export_name,
        export_path=JianYing_Export_Dir,
        Frame=50,
        export_sub =False
    )
    _ins._Export(Export_Options)
    _ins._Close()


def jianying_combine_json(Project_Dir, videos_list):
    my_jy_element = JianYingContainer(Project_Dir)
    # 从config文件中获得配置信息
    #######################################  video 视频      #######################################
    my_jy_element.combine_videos(videos_list)

    # 保存
    my_jy_element.draft.Save()


if __name__ == "__main__":
    # main()
    jianying_create_project()
