# Lenovo-"Xie Yan"
import os

Making_folder = r'F:\VideosCache\MakingDirs'
Input_folder = os.path.join(Making_folder, 'InputVideos')  # 输入文件夹
Output_folder = os.path.join(Making_folder, 'OutputVideos')  # 输出文件夹
Main_Video_Folder = os.path.join(Input_folder, 'Mainvideos')  # 目标文件夹
video_Out_folder = os.path.join(Main_Video_Folder, "Out")  # 输出文件夹
LingFox_video_folder = os.path.join(video_Out_folder, 'Finish')  # 灵狐输出文件夹

video_time_index_info = os.path.join(Main_Video_Folder, "video_info.txt")  # 存储视频time等，用于ffmpeg的视频分割
video_file_name_copy = os.path.join(Main_Video_Folder, 'file.txt')  # ffmpeg的视频合成，根据相应的格式书写
composite_file = os.path.join(video_Out_folder, 'output.mp4')  # 合成的视频

JianYing_Export_Dir = r"F:\VideosCache\MakingDirs\OutputVideos\Jianying"  # 剪映视频导出文件夹
JianYing_Exe_Path = r"D:\ProgramFiles\VideoDesign\Jianying\JianyingPro"  # 剪映安装可执行文件文件夹

Combine_mp4 = os.path.join(Output_folder, 'combine.mp4')  # 拼接的视频文件
Created_mp4 = os.path.join(Output_folder, 'created.mp4')  # 二次创作，去重的视频

PICTURERESOURCE_DIR = os.path.join(Input_folder, 'PictureResource')  # 画中画文件夹
RUBBISHCACHE_DIR = os.path.join(Input_folder, 'RubbishCache')  # 图片cache文件夹
REINDEX_JPG_DIR = os.path.join(RUBBISHCACHE_DIR, 'ReIndex_Jpg')  # 重排后的图片文件存储在这里

Output_finish = os.path.join(Output_folder, 'Finish')  # 图片转视频的最终输出文件

Content_Json_File = r'/Datastorage\\content.json'  # created配置json文件
Src_Json_File = r'/Datastorage\\src.json'  # src字幕文件的配置json文件

Working_Exe_Path = os.getcwd()  # 主工作目录

Data_Storage_Dir = os.path.join(Working_Exe_Path, 'Datastorage')  # "D:\Code\Python\Tiktok\Datastorage"
Data_Storage_storage_Dir = os.path.join(Data_Storage_Dir, 'storage')  # "D:\Code\Python\Tiktok\Datastorage\storage"
User_Info_Db = os.path.join(Data_Storage_storage_Dir,
                            'user_info.db')  # "D:\Code\Python\Tiktok\Datastorage\storage\user_info.db"
User_Cookie_Dir = os.path.join(Data_Storage_storage_Dir,
                              'cookies')  # "D:\Code\Python\Tiktok\Datastorage\storage\cookies"
Error_Html_Dir = os.path.join(Data_Storage_storage_Dir,
                              'error_html')  # "D:\Code\Python\Tiktok\Datastorage\storage\error_html"
Browser_Storage_Dir = os.path.join(Working_Exe_Path, 'Browser')

Datastorage_Image_Dir = os.path.join(Data_Storage_Dir, 'image')
Verication_Tk_Dir = os.path.join(Datastorage_Image_Dir, 'verication')  # 验证码位置

Chrome_Extension_Dir = os.path.join(Browser_Storage_Dir, "storage/extensions")

# clash文件位置
Clash_Exe_Path = r"F:\Auxiliary Software\Clash\Clash for Windows.exe"
Clash_Config_List_Yml = r"C:\Users\Lenovo\.config\clash\profiles\list.yml"
Clash_Proxies_Yaml = r'C:\Users\Lenovo\.config\clash\profiles\clash.yaml'


# tiktok UserAvter
User_Avter_Dir = r'F:\VideosCache\UserAvter'

