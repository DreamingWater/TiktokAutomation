"""
    BiliBili Schema
    Why?
        For Some Video, It is unnecessary for you to convert hole Video List. So You Can Customize them.
"""
# Input Example : https://api.bilibili.com/x/web-interface/view?bvid=BV1vG41157Px -> Data -> Pages
# Output Example [820192502,807216248,...(Cid)]
def Default(Pages:list): return [fn["cid"] for fn in Pages]
# def ASDB(Pages:list): return [fn["cid"] for fn in Pages if "弹幕" not in fn["part"]]
