# Lenovo-"Xie Yan"
from __future__ import annotations

import sqlite3 as sl

from tiktok_config import User_Info_Db
from loguru import logger

# 连接数据库
def sqlite_connect(save_db_name):
    sl_con = sl.connect(save_db_name)
    return sl_con


# 执行命令
def sqlite_run_command(sl_con_obj, command: str, data: tuple | None = None):
    try:
        c = sl_con_obj.cursor()
        if data is not None:
            c.execute(command, data)
        else:
            c.execute(command)
        sl_con_obj.commit()
        return c
    except Exception as e:
        print(e)
        print('an error in %s' % command)
        sl_con_obj.rollback()
        return False


# judge table exist or not
def judge_table_exist_or_not(sl_con_obj, table_name: str) -> bool:
    # 查询是否存在表
    table_check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = sqlite_run_command(sl_con_obj, table_check_query, (table_name,))
    if result is not False:
        one_result = result.fetchone()
        if one_result is None or one_result == []:
            return False
        return True
    return False


# 从数据库中获取没有注册tk的数据
def get_raw_login_info():
    login_info = []  # 登录信息
    sl_con = sqlite_connect(User_Info_Db)
    # 查询last_login改变过的
    select_cmd = "SELECT * FROM UserInfo WHERE LAST_LOGIN=101"
    c = sl_con.cursor()
    c.execute(select_cmd)
    # 获取查询结果
    results = c.fetchall()
    sl_con.close()
      for result in results:
        login_info.append({'email': result[1], 'password': result[2]})
    if len(login_info) == 0:
        logger.error('The db data is None.')
    return login_info # [{'email': '***@outlook.com', 'password': '***'}]


def update_the_tb(email_, meta, value):
    sl_con = sqlite_connect(User_Info_Db)
    res = None
    if type(value) == str:
        command = 'UPDATE UserInfo SET "%s" = "%s" WHERE EMAIL="%s"'%(meta, value, email_)
    else:
        command = 'UPDATE UserInfo SET "%s" = %s WHERE EMAIL="%s"'%(meta, value, email_)
    res = sqlite_run_command(sl_con, command=command) # 执行命令

    if res:
        logger.info('succeed to update the {}:{} based email:{}'.format(meta,value,email_))
    sl_con.close()  # 关闭数据库