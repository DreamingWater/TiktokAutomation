"""
Read And Write JianYing Config
"""

import os , json , time

class Draft_Content_Json:
    def __init__(self,path:str="",content:str="") -> None:
        if path: self.Config = json.loads(os.open(path,"r",encoding="utf-8").read())
        if content: self.Config = json.loads(content)

    def Parse(self):
        ...