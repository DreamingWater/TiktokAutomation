import sys
sys.path.append("..")
from . import Jy_Warp
import uiautomation

def Recognize_Subtitle(filename:str,filepath:str,export_options:Jy_Warp.Export_Options,jianying_instance:Jy_Warp.Instance):
    """
        Recognize Subtitle
        Langugage Support Chinese and English.
        It Will Open an instance of jianying if not given.
        filepath,filename,exportoptions is needed.
    """
    while jianying_instance._detect_viewport() != 1: Jy_Warp.lag()
    jianying_instance._Append_Media(path=filepath,name=filename)
    jianying_instance._Drag_To_Track(0)
    jianying_instance.click_text_button_position() # 点击文本
    jianying_instance._To_column("文本","新建文本","智能字幕")
    uiautomation.Click(x=jianying_instance.get_text_position_relative_x(),y=int(jianying_instance._VETreeMainCellItem("识别歌词").BoundingRectangle.bottom))
    while jianying_instance._detect_viewport() == 2 : Jy_Warp.lag()
    jianying_instance._Export(export_options)
    # jianying_instance._clear_all_media()