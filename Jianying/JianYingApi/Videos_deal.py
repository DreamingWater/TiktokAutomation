# Lenovo-"Xie Yan"
import uuid

from Jianying.Scripts.json_parse import get_element_from_json
from Jianying.Scripts.time_deal import get_video_duration
from Jianying.JianYingApi.myconfig import *

_on_video_track = None  # track_for_video 的 ID 暂存

class VideoElement:
    def __init__(self, draft, video_path):
        self.draft = draft  # Draft 操作句柄
        self.video_path = video_path  # 文件路径
        self.video_name = video_path.split('\\')[-1][:-4]  # 截取文件名
        self.video_duration = get_video_duration(video_path)  # 获取视频文件时长，为us


    def deal_speed(self, speed):
        video_speed_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=self.video_name + "_speed"))
        self.draft.Content.AddMaterial(Mtype='speeds', Content={
            "curve_speed": null,
            "id": video_speed_id,
            "mode": 0,
            "speed": speed,
            "type": "speed"
        })
        return video_speed_id

    def deal_meta_json(self):
        self.draft.Meta.Import2Lib(path=self.video_path, metetype="video", duration=self.video_duration)

    def deal_canvas(self):
        video_canvas_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=self.video_name + "_canvas"))
        self.draft.Content.AddMaterial(Mtype='canvases', Content=
        {"album_image": "",
         "blur": 0.0,
         "color": "",
         "id": video_canvas_id,
         "image": "",
         "image_id": "",
         "image_name": "",
         "source_platform": 0,
         "team_id": "",
         "type": "canvas_color"
         })
        return video_canvas_id

    def deal_sound_channel(self):
        video_sound_channel_mappings_id = str(
            uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=self.video_name + "_sound_channel"))
        self.draft.Content.AddMaterial('sound_channel_mappings', Content={
            "audio_channel_mapping": 0,
            "id": video_sound_channel_mappings_id,
            "is_config_open": False,
            "type": "none"
        })
        return video_sound_channel_mappings_id

    def deal_material(self):
        video_material_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=self.video_name + "_material"))
        self.draft.Content.AddMaterial(Mtype="videos",
                                       Content={"category_name": "local", "extra_type_option": 0, "has_audio": true,
                                                "id": video_material_id,
                                                "material_name": self.video_name, "path": self.video_path,
                                                "type": "video"}
                                       )
        return video_material_id

    def composite_to_track(self, source_start, source_duration, render_index, alpha=1.0, scale=None, rotation=0.0,
                           transform=None,
                           speed=1.0, flip=None,
                           extra_material=None, new_track=True):
        global _on_video_track
        if new_track or _on_video_track is None:
            _on_video_track = self.draft.Content.NewTrack(TrackType="video")  # 添加视频track
        video_track_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=self.video_name + "_track"))
        if scale is None:
            scale = {"x": 1.0, "y": 1.0}
        if transform is None:
            transform = {"x": 0.0, "y": 0.0}
        if flip is None:
            flip = {"horizontal": false, "vertical": false}
        # 配置 extra_material_refs
        extra_material_refs = [
            self.deal_sound_channel(),
            self.deal_canvas(),
            self.deal_speed(speed)
        ]
        if extra_material is not None:
            extra_material_refs.extend(extra_material)
        # 需要更新的参数字典
        _track_segment = {
            "id": video_track_id,
            "material_id": self.deal_material(),
            "speed": speed,
            "render_index": render_index,
            "source_timerange": {
                "duration": source_duration,
                "start": source_start
            },
            "target_timerange": {
                "duration": int(source_duration / speed),
                "start": 0
            },
            "extra_material_refs": extra_material_refs,
            "clip": {
                "alpha": alpha,
                "flip": flip,
                "rotation": rotation,
                "scale": scale,
                "transform": transform
            },
            "track_attribute": 0,
            "volume": 0.0
        }
        # track部分的video参数字典全集，来自剪影，
        _track_content = get_element_from_json(desired_key='video', json_file='videotrack.json', Meta='track')
        _track_content.update(_track_segment)
        self.draft.Content.Add2Track(Track_id=_on_video_track["id"], Content=_track_content)

    def add_one_video(self, main_video_duration, render_index, source_start=None,
                      alpha=1.0, scale=None, rotation=0.0, transform=None,
                      extra_material=None, flip=None, new_track=True):
        self.deal_meta_json()
        # init some data
        video_speed = 1.0
        source_duration = self.video_duration
        if source_start is None:
            source_start = 0  # 初始化默认为整个视频长度
            if main_video_duration is not None:
                source_start, source_duration, video_speed = self.adjust_video_to_main(
                    main_video_duration)  # 对视频镜像裁剪，掐头去尾,然后设置播放速度
        else:
            source_duration = self.video_duration - source_start  # 截取前面的部分
            #print('begin to use source_duration')
        self.composite_to_track(source_start=source_start, source_duration=source_duration, render_index=render_index,
                                alpha=alpha, scale=scale, rotation=rotation, transform=transform, speed=video_speed,
                                extra_material=extra_material, flip=flip, new_track=new_track)
        return self.draft, self.video_duration  # 返回draft实例，并且返回视频的时长

    def adjust_video_to_main(self, main_video_duration):
        # cut the video
        source_start = 10 * 10 ** 6  # 10s
        source_duration = int(self.video_duration * 0.95) - source_start

        if source_duration <= 0:
            source_duration = source_duration - source_start
        video_speed = source_duration / main_video_duration
        return source_start, source_duration, float(video_speed)
