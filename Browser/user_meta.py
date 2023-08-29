# Lenovo-"Xie Yan"
import math
import os
import random
import string

from utils.sqlite_db import sqlite_connect, sqlite_run_command, judge_table_exist_or_not
from tiktok_config import User_Info_Db
from loguru import logger
OUTLOOK_EMAIL = '%s@outlook.com'


class RandomUserMeta:
    def __init__(self) -> None:
        self.email = ''
        self.password = ''
        self.firstname = ''
        self.lastname = ''
        self.birth_year = 2000
        self.birth_month = 1
        self.birth_day = 1
        self.country = '北京'
        self.usermeta = False  # 是否已经生成user info
        # this_file_path = __file__ # 当前文件的完全路径
        # self.file_dir_path = os.path.dirname(this_file_path) # 'D:\\Code\\Python\\Tiktok\\Browser'

    def request_user_meta(self,email_change=True):
        """
        生成一次虚拟用户数据
        :param email_change False代表不需要重新生成 True表示需要重新生成
        :return 密码输入定位元素:
        """
        if email_change:
            self.email = self.random_email_or_passwd(14)  # 12位的邮箱
            self.email = OUTLOOK_EMAIL % self.email
        if self.usermeta:  # 如果之前已经生成该数据就退出
            return

        self.password = self.random_email_or_passwd(12, passwd=True)  # 12位的密码
        self.random_name()  # name
        self.random_birth_data()  # birth data
        self.usermeta = True

    def random_name(self):
        self.firstname = self.random_name_string(6)
        last_name_length = random.randint(4, 6)  # 名字的长度
        self.lastname = self.random_name_string(last_name_length)

    # 生成 出生年月日
    def random_birth_data(self):
        self.birth_year = random.randint(1980, 2001)
        self.birth_month = random.randint(1, 12)
        self.birth_day = random.randint(1, 26)

    # 此函数用于生成email或者passwd的字符串
    def random_email_or_passwd(self, str_length: int, passwd=False):
        # 随机生成字母和数字的位数
        assert str_length > 6, "the length of the random string is too short"
        num_count = random.randint(1, math.floor(str_length / 2))
        letter_count = str_length - num_count

        # 随机抽样生成数字序列
        num_list = [random.choice(string.digits) for _ in range(num_count)]
        # 随机抽样生成字母序列
        letter_list = [random.choice(string.ascii_letters) for _ in range(letter_count)]
        # 合并字母数字序列
        for index, num in enumerate(num_list):
            letter_list_length = len(letter_list)  # 获取letterlist长度
            letter_list.insert(random.randint(1, letter_list_length), num)  # 将数字插入到字符中拼接,设置开头必为字母
        if passwd:
            letter_list.insert(random.randint(1, len(letter_list) - 1), '@')  # 将数字插入到字符中拼接
        # 生成目标结果字符串
        result = "".join(letter_list)
        return result

    # 此函数用于生成name的字符串
    def random_name_string(self, str_length: int):
        # 随机抽样生成字母序列
        letter_list = [random.choice(string.ascii_letters) for _ in range(str_length)]
        # 生成目标结果字符串
        result = "".join(letter_list)
        return result.lower()

    def save_user_data(self):
        sl_con = sqlite_connect(User_Info_Db)
        if not judge_table_exist_or_not(sl_con, 'UserInfo'):  # 没有表单就创建一个
            create_user_info(sl_con)
            logger.info('create the sqlite')
        # 将数据保存到table中
        self.insert_data_to_db(sl_con_obj=sl_con)
        # 关闭数据库
        sl_con.close()

    def insert_data_to_db(self, sl_con_obj):
        command = """
        INSERT INTO UserInfo (EMAIL,PASSWORD,FIRST_NAME,LAST_NAME,BIRTH_YEAR,BIRTH_MONTH,BIRTH_DATA,COUNTRY,
        LAST_LOGIN,LAST_COMMENT) 
              VALUES (?,?,?,?,?,?,?,?,?,?)
        """
        sqlite_run_command(sl_con_obj=sl_con_obj, command=command,
                           data=(self.email, self.password, self.firstname, self.lastname, self.birth_year,
                                 self.birth_month, self.birth_day, self.country,
                                 "0101", "0101"))






# 创建user_info table
def create_user_info(sl_con):
    create_table_command = """
    CREATE TABLE UserInfo(
                       ID           INTEGER PRIMARY KEY AUTOINCREMENT,
                       EMAIL          CHAR(30)    NOT NULL,
                       PASSWORD       CHAR(30)    NOT NULL,
                       FIRST_NAME     CHAR(20)    NOT NULL,
                       LAST_NAME      CHAR(20)    NOT NULL,
                       BIRTH_YEAR     INT         NOT NULL,
                       BIRTH_MONTH    INT         NOT NULL,
                       BIRTH_DATA     INT         NOT NULL,
                       COUNTRY        TEXT        NOT NULL,
                       LAST_LOGIN     INT    NOT NULL,
                       LAST_COMMENT   INT    NOT NULL
                    );
     """
    sqlite_run_command(sl_con, create_table_command)
