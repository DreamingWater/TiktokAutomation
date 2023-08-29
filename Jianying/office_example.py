# Lenovo-"Xie Yan"

import JianYingApi, uuid


#########Step1 新建视频项目

d = JianYingApi.Drafts.Create_New_Drafts(r"F:\VideosCache\Drafts\PulpFiction") # Create New Project
# Create Two Tracks
video_track = d.Content.NewTrack(TrackType="video")
efect_track = d.Content.NewTrack(TrackType="effect")
# Add Video Material
video_path = r"C:\Users\Lenovo\Desktop\Youtube\test.mp4"
video_name = "PulpFiction"
video_material_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS,name=video_name+"_material"))
video_track_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS,name=video_name+"_track"))
d.Meta.Import2Lib(path=video_path,metetype="video")
d.Content.AddMaterial(Mtype="videos",Content={"category_name":"local","extra_type_option":0,"has_audio":True,"id":video_material_id,
                            "material_name":video_name,"path":video_path,"type":"video"})
d.Content.Add2Track(Track_id=video_track["id"],Content=
        {
          "id":video_track_id,
          "material_id":video_material_id,
          "visible":True,
          "volume":1,
          "source_timerange": {
            "duration": 605000000,
            "start": 2050633333
          }, "target_timerange": {
            "duration": 605000000,
            "start": 0
          }})
# Add Effects
effect_name = "蓝色丝印"
effect_resource_id="7131985730791805448"
effect_id="4097661"
effect_material_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS,name=effect_name+"_material"))
effect_track_id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS,name=effect_name+"_track"))
d.Content.AddMaterial(Mtype="video_effects",Content=
  {"apply_target_type":2,"effect_id":effect_id,"id":effect_material_id,"name":effect_name,"render_index":0,"effect_resource_id":effect_resource_id,
   "type":"video_effect","value":1})
d.Content.Add2Track(Track_id=efect_track["id"],Content=
        {
          "id": effect_track_id,
          "material_id": effect_material_id,
          "render_index": 11000,
          "speed": 1,
          "target_timerange": {
            "duration": 500600000,
            "start": 0
          },
          "visible": True,
          "volume": 1
        }
    )
# Save
d.Save()

#########Step2 打开剪映识别
ins = JianYingApi.Jy_Warp.Instance(JianYing_Exe_Path=r"D:\ProgramFiles\VideoDesign\Jianying\JianyingPro")