# Lenovo-"Xie Yan"


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import math
import random
import time

# 生成鼠标移动轨迹
def generate_path(x, y, width, height, duration):
    path = []
    t = 0.0
    while t < duration:
        # 计算当前时间占总时间的比例
        ratio = t / duration

        # 计算鼠标当前位置
        px = x + width * curve(ratio)
        py = y + height * curve(ratio)

        # 计算鼠标当前速度
        speed = random.uniform(0.4, 0.6)

        # 添加位置和速度到轨迹中
        path.append((int(px), int(py), speed))

        # 计算下一个时间点
        t += speed

    return path

# 生成曲线
def curve(t):
    return math.sin(t * math.pi / 2)

# 模拟鼠标移动
def move_mouse(driver, element, duration):
    # 模拟鼠标移动
    actions = ActionChains(driver)
    actions.move_to_element(element)

    # 生成鼠标移动轨迹
    x, y = element.location['x'], element.location['y']
    width, height = element.size['width'], element.size['height']
    path = generate_path(x, y, width, height, duration)

    # 按照轨迹移动鼠标
    for p in path:
        actions.move_by_offset(p[0], p[1])
        actions.perform()
        time.sleep(p[2])


