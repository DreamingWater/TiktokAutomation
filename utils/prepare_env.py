"""
    Downlaod ffmpeg / aria2 By Choco
            Jianying By aria2
"""
from subprocess import run , DEVNULL

def f_a():
    return run("choco","install","-y","ffmpeg","aria2","7zip",stderr=DEVNULL,stdout=DEVNULL)

def DownloadJianYing():
    URL = "https://lf3-package.vlabstatic.com/obj/faceu-packages/Jianying_pro_3_3_0_9035_jianyingpro_0.exe"
    aria2(URL," --check-certificate=false ","./jy.exe")

def aria2(url:str,header:str,p_name:str):
    return run(" ".join(["aria2c","-x","16","-s","16","-k","1M","-o",p_name,url,header])
    ,stdout=DEVNULL,stderr=DEVNULL )

def ga():
    """
        For Github Action
    """
    import sys
    sys.path.append('..')
    from JianYingApi import JianYingApi as Api
    f_a() , DownloadJianYing() , Api.Logic_warp._install_JianYing("jy.exe")