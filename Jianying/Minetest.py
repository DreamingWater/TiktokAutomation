# Lenovo-"Xie Yan"
import JianYingApi, uuid

# Special data
false = "_false_"
null = "_null_"
true = "_true_"

#########Step1 新建视频项目

d = JianYingApi.Drafts.Create_New_Drafts(r"F:\VideosCache\Drafts\PulpFiction")  # Create New Project
# Create Two Tracks
video_track = d.Content.NewTrack(TrackType="video")
# Add Video Material
video_path = r"C:\Users\Lenovo\Desktop\Youtube\test.mp4"
video_name = video_path.split('\\')[-1][:-4]
video_material_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=video_name + "_material"))
video_track_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=video_name + "_track"))
video_speed_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=video_name + "_speed"))
video_canvas_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=video_name + "_canvas"))
video_sound_channel_mappings_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=video_name + "_sound_channel"))
d.Meta.Import2Lib(path=video_path, metetype="video")
d.Content.AddMaterial(Mtype="videos", Content={"category_name": "local", "extra_type_option": 0, "has_audio": true,
                                               "id": video_material_id,
                                               "material_name": video_name, "path": video_path, "type": "video"}
                      )
d.Content.AddMaterial(Mtype='canvases', Content=
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
 }
                      )
d.Content.AddMaterial('sound_channel_mappings',Content={
    "audio_channel_mapping": 0,
    "id": video_sound_channel_mappings_id,
    "is_config_open": False,
    "type": ""
})

d.Content.AddMaterial(Mtype='speeds', Content={
    "curve_speed": null,
    "id": video_speed_id,
    "mode": 0,
    "speed": 1.0,
    "type": "speed"
})

d.Content.Add2Track(Track_id=video_track["id"], Content=
{
    "id": video_track_id,
    "material_id": video_material_id,
    "visible": true,
    "volume": 1,
    "source_timerange": {
        "duration": 198666666,
        "start": 0
    },
    "target_timerange": {
        "duration": 198666666,
        "start": 0
    },
    "extra_material_refs": [
        video_sound_channel_mappings_id,
        video_speed_id,
        video_canvas_id
    ],
    "clip": {
        "alpha": 1.0,
        "flip": {
            "horizontal": false,
            "vertical": false
        },
        "rotation": 0.0,
        "scale": {
            "x": 1.0,
            "y": 1.0
        },
        "transform": {
            "x": 0.0,
            "y": 0.0
        }
    },
})

d.Save()

#########Step2 打开剪映识别
import JianYingApi as Api
import multiprocessing
multiprocessing.freeze_support()
_ins = Api.Jy_Warp.Instance(Start_Jy=True,JianYing_Exe_Path="D:\ProgramFiles\VideoDesign\Jianying\JianyingPro\JianyingPro.exe")

Api.Logic_warp.echo("Creat Main Instance.")
while Api.Logic_warp._has_running() == False: Api.Logic_warp.lag()
_ins._Start_New_Draft_Content(wait=True)  # 进入主页面
# {
#     "adjust_params": [],
#     "algorithm_artifact_path": "",
#     "apply_target_type": 0,
#     "bloom_params": null,
#     "category_id": "",
#     "category_name": "",
#     "effect_id": "871337",
#     "enable_skin_tone_correction": false,
#     "exclusion_group": [],
#     "face_adjust_params": [],
#     "formula_id": "",
#     "id": "D6A8442A-6083-408b-B7C0-19D7F2E5A962",
#     "intensity_key": "",
#     "name": "柔光",
#     "panel_id": "",
#     "path": "D:\\ProgramFiles\\VideoDesign\\Jianying\\JianyingPro\\4.0.1.9886\\Resources\\MixMode\\042aa15b71b1e17bca0bd928eec6fba7",
#     "platform": "all",
#     "resource_id": "6758325439212556814",
#     "source_platform": 0,
#     "sub_type": "none",
#     "time_range": null,
#     "type": "mix_mode",
#     "value": 1.0,
#     "version": ""
# }