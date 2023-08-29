# Lenovo-"Xie Yan"
import os
import uuid
from Jianying.JianYingApi.myconfig import *
from Jianying.Scripts.json_parse import get_element_from_json


class EffectElement:
    def __init__(self, draft):
        self.draft = draft  # Draft 操作句柄

    def effect_update_material(self, effect_json, adjust_params):
        if not type(adjust_params) == list:
            effect_json['value'] = adjust_params if adjust_params is not None else 1.0
        self.draft.Content.AddMaterial(Mtype="effects", Content=effect_json)  # effects
        # return effect_json

    def special_effect_update_material(self, effect_json: dict, adjust_params):
        effect_json.update({"adjust_params": adjust_params})
        self.draft.Content.AddMaterial(Mtype="video_effects", Content=effect_json)  # video_effects
        # return effect_json

    def deal_effect_material(self, effect_id, adjust_params=None,
                             effect_type="effect_filter"):
        # 加载不同的json文件
        effect_material_id = str(uuid.uuid1())
        effect_json = get_element_from_json(desired_key=effect_id, json_file='%s.json' % effect_type)  # 需要加载的json文件
        effect_json['id'] = effect_material_id
        # 根据需要对dict进行二次封装

        if effect_type == "effect_filter":
            self.effect_update_material(effect_json, adjust_params)
        elif effect_type == "effect_video":
            self.draft.Content.AddMaterial(Mtype="effects", Content=effect_json)
        else:
            self.special_effect_update_material(effect_json, adjust_params)

        return effect_material_id

    def composite_to_track(self, which_effect, render_index, _duration, speed=1,
                           start=0, adjust_params=None, effect_type='effect_filter'):
        track_type = "filter" if effect_type == 'effect_filter' else "effect"
        effect_track = self.draft.Content.NewTrack(TrackType=track_type)  # 添加视频track
        effect_track_id = str(uuid.uuid1())
        self.draft.Content.Add2Track(Track_id=effect_track["id"], Content=
        {
            "id": effect_track_id,
            "material_id": self.deal_effect_material(which_effect, adjust_params=adjust_params,
                                                     effect_type=effect_type),
            "speed": speed,
            "render_index": render_index,
            "target_timerange": {
                "duration": _duration,
                "start": start
            },
            "visible": true,
            "volume": 1
        }
                                     )

    def add_one_effect(self, effect_id, render_index=10000, duration=-1, effect_type='effect_filter', start=0,
                       adjust_params=None):
        effect_uuid = None  # effect_uuid
        if effect_type == 'effect_video':
            effect_uuid = self.deal_effect_material(effect_id, adjust_params=adjust_params,
                                                    effect_type=effect_type)  # 取到effect_id用于video_extra_material
        else:
            self.composite_to_track(which_effect=effect_id, render_index=render_index, _duration=duration,
                                    start=start, adjust_params=adjust_params, effect_type=effect_type)
        return self.draft, [effect_uuid]  # effect_uuid 列表形式更好处理
