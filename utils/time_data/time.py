# Lenovo-"Xie Yan"

from datetime import datetime

# 获取今天的月日信息
def get_today():
    today = datetime.today()
    return int(today.strftime("%m%d"))
