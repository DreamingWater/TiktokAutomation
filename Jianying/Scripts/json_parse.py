# Lenovo-"Xie Yan"
import json, os


# 读取 配置文件，并数据模板返回
def get_element_from_json(desired_key, json_file, Meta='effects') -> dict:
    json_file_location = os.path.join(os.getcwd(),'Jianying', 'JianYingApi', 'blanks', json_file)
    json_data = None
    with open(json_file_location, encoding='utf-8') as f:
        json_data = json.load(f)
    effects = json_data[Meta]  # 获取effects dict
    effects_key_list = [key for key in effects.keys()]  # dict 的key 组成列表
    if isinstance(desired_key, int):
        assert desired_key < len(effects_key_list), 'you should decrease the number: which_effect'
        desired_key = effects_key_list[desired_key]
    effect_json = effects[desired_key]
    return effect_json
