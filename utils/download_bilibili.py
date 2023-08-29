import os
import requests
from . import bilibili_schema
from . import prepare_env
from . import media_type
from . import etcs
def bilibili(i:dict)->list:
    # Sourcer 
    # 1: api接口
    _k = []
    if "Path" in i : _path = i["Path"]
    else: _path = "./assets/"
    headers = {"User-Agent":"Mozilla/5.0"}
    pages = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={i['Bv']}",headers=headers)
    pages.encoding = 'utf-8'
    pages = pages.json()["data"]["pages"]
    if "P" in i and i["P"] !=None: cids = [fn["cid"] for fn in pages if fn["page"]-1 in i["P"]]
    elif "Schema" in i and i["Schema"] != None: cids = getattr(bilibili_schema,i["Schema"])(pages)
    else: cids = bilibili_schema.Default(pages)
    etcs.echo(f"Start Download {i['Bv']} _ {cids}")
    etcs.echo(cids)
    for j in cids:
        download_url = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={i['Bv']}&cid={j}&otype=json&&platform=html5&high_quality=0",headers=headers)
        download_url.encoding='utf-8'
        download_url = download_url.json()["data"]["durl"][0]["url"]
        pname =_path +  f"{i['Bv']}-{cids.index(j)+1}.mp4" if len(cids) >1 else _path + f"{i['Bv']}.mp4"
        prepare_env.aria2(url=download_url,p_name=pname,header='  --check-certificate=false  --header="Refer:https://www.bilibili.com" --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0" ')
        _k.append(media_type.Media_Type(path=os.path.dirname(os.path.abspath(pname)),
                                        filename=os.path.basename(os.path.abspath(pname))))
    return _k