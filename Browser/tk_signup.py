# Lenovo-"Xie Yan"
import json
import pickle
import random
import time
from time import sleep
import string
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from PIL import Image
import requests
from selenium.webdriver.support.select import Select
# from lxml import etree
import re
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support.select import Select
from decouple import config
from selenium.webdriver.common.by import By

from Browser.outlook_login import OutlookMailLogin
from Browser.outlook_register import OutlookMailRegister
from Source.chrome.Chrome import run_chrome_thread, shut_chrome_thread
from tiktok_config import Working_Exe_Path, User_Cookie_Dir, Chrome_Extension_Dir
from utils.common import common_download_image
import undetected_chromedriver as uc

from utils.sqlite_db import update_the_tb
from utils.time_data.time import get_today
from loguru import logger


class TkSignup:
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.tiktok.com/'
        self.signup_url = 'https://www.tiktok.com/signup/phone-or-email/email'
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')
        self.country = 'None'
        # user agent
        self.browser_port = 9222
        run_chrome_thread(self.browser_port)
        time.sleep(5)
        # 启用带插件的浏览器

        option = webdriver.ChromeOptions()
        # option = uc.ChromeOptions()
        # 加载用户配置 绕过登录
        # option.add_argument(f"--user-data-dir=C:\\Users\\Lenovo\\AppData\\Local\\Temp\\tmpuabg9cht\\Default")
        # option.add_argument(" --profile-directory=Profile 1")
        # start clean 插件
        # start_clean_plugin = os.path.join(Chrome_Extension_Dir, "extension_pooaemmkohlphkekccfajnbcokjlbehk")
        # option.add_argument(f"--load-extension=%s" % start_clean_plugin)
        # option.add_argument("--disable-blink-features=AutomationControlled")
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option("debuggerAddress", "127.0.0.1:%s" % self.browser_port)

        # from fake_useragent import UserAgent
        # ua = UserAgent()
        # user_agent = ua.random
        # option.add_argument(f'user-agent={user_agent}')
        # 添加插件的crx文件
        # option.add_extension(r"D:\Code\Python\Tiktok\Browser\storage\clean.crx")  # 加载插件

        # option.add_argument("")
        # 创建带插件的浏览器对象
        # option.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        # self.browser = uc.Chrome(options=option)
        chrome_driver_path = os.path.join(self.broswer_dir, "chromedriver.exe")
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, options=option)

        # self.browser = webdriver.Edge(path)

        # with open(os.path.join(Working_Exe_Path, 'Browser', 'storage', 'stealth.min.js')) as f:
        #     js = f.read()
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })
        self.wait = WebDriverWait(self.browser, 10)
        self.verication_success = False

    # 启动 clean 插件
    def click_clean_button_crt(self):
        time.sleep(5)
        self.wait_xpath('.//img[@class="inserted-btn mtz"]')
        clean_button = self.browser.find_element(By.XPATH, './/img[@class="inserted-btn mtz"]')
        clean_button.click()

    # outlook email 验证码
    def outlook_email_verication_code(self, outlook):
        look_up_time = 0
        while True:
            email_result = outlook.find_the_tk_email()  # 读取邮箱
            look_up_time += 1
            if email_result is False:
                outlook.browser.refresh()
                if look_up_time >= 4:
                    logger.error('An error in the outlook mailbox')
                time.sleep(10 + look_up_time * 5)
            else:
                logger.info('the tiktok verication code is: {}'.format(email_result))
                return email_result

    # outlook 验证码
    def outlook_email_obj(self, email, password):
        outlook_login = OutlookMailLogin()
        outlook_login.login(email, password)
        outlook_login.browser.minimize_window()
        return outlook_login

    def test_outlook_email(self):
        '''
        :return:
        '''
        outlook = OutlookMailRegister()
        outlook.browser.get(outlook.base_url)
        try:
            test_email_address = input('email address??')
            res = self.outlook_email_verication_code(outlook)
            print(res)
            self.debug_stop()
        except Exception as e:
            print(e)

    def get_signup_website1(self, email, password):
        '''
        :return:
        '''
        logger.info('ready to use selenium to get signup website')
        self.browser.get('http://baidu.com')
        time.sleep(5)
        input_ = self.browser.find_element(By.XPATH, './/input[@id="kw"]')
        is_disabled = input_.get_attribute("value") is not None
        print(is_disabled)
    def get_signup_website(self, email, password):
        '''
        :return:
        '''
        self.check_ip_country()
        logger.info('ready to use selenium to get signup website')
        self.browser.get(self.signup_url)
        # # 生成user info 数据
        self.browser.maximize_window()
        try:
            self.click_clean_button_crt()
            self.browser.refresh()
            time.sleep(random.random() + 5)
            # # 填写邮箱和密码
            self.add_email_passwd(email, password)
            logger.info('email is {}, passwd is {}'.format(email, password))

            # # 填写birth信息
            # self.add_birth_infomation(random.randint(1, 12), random.randint(1, 26),
            #                           random.randint(1980, 2001))
            input_test = input('please input sth')

            # 等待
            # 图片验证码
            vericaiton_state = self.deal_verication_code()
            if vericaiton_state is False:  # 访问太频繁
                logger.error('Too much try in this duration')
                a = input('please input sth to deal this problem-----1')
                if a == '1':
                    update_the_tb(email, 'LAST_LOGIN', get_today())
                    update_the_tb(email, 'COUNTRY', self.country)
                    self.browser.close()
                    return
            if self.judge_button_clickable('.//button[@data-e2e="send-code-button"]'):
                logger.info('success to send the email code')
            self.browser.close()

        except Exception as e:
            print(e)
            self.browser.close()
    def get_signup_website_(self, email, password):
        '''
        :return:
        '''
        self.check_ip_country()
        logger.info('ready to use selenium to get signup website')
        self.browser.get(self.signup_url)
        # # 生成user info 数据
        outlook = self.outlook_email_obj(email, password)
        self.browser.maximize_window()
        try:

            self.click_clean_button_crt()
            self.browser.refresh()
            time.sleep(random.random() + 5)
            # # 填写邮箱和密码
            self.add_email_passwd(email, password)
            logger.info('email is {}, passwd is {}'.format(email, password))

            # # 填写birth信息
            self.add_birth_infomation(random.randint(1, 12), random.randint(1, 26),
                                      random.randint(1980, 2001))
            # 等待
            # 图片验证码
            vericaiton_state = self.deal_verication_code()
            if vericaiton_state is False:  # 访问太频繁
                logger.error('Too much try in this duration')
                a = input('please input sth to deal this problem-----1')
                if a == '1':
                    self.write_cookies(outlook.email)
                    update_the_tb(email, 'LAST_LOGIN', get_today())
                    update_the_tb(email, 'COUNTRY', self.country)
                    self.browser.close()
                    return
            logger.info('success to send the email code')
            # # 获取验证码
            verication_code = self.outlook_email_verication_code(outlook)
            # # # 填写验证码
            verication = self.browser.find_element(By.XPATH, './/div[contains(@class,"DivCodeInputContainer")]//input')
            webdriver.ActionChains(self.browser).move_to_element(verication).perform()
            self.browser.execute_script("arguments[0].click();", verication)
            verication.send_keys(verication_code)
            # # 提交表格
            button = self.browser.find_element(By.XPATH, './/button[@type="submit"]')
            self.browser.execute_script("arguments[0].click();", button)
            # 注册用户名？？
            self.random_user_name()

            cookie_button = self.is_exist('.//tiktok-cookie-banner')
            if cookie_button:
                self.click_cookie_button()

            self.write_cookies(outlook.email)
            update_the_tb(email, 'LAST_LOGIN', get_today())
            update_the_tb(email, 'COUNTRY', self.country)
            outlook.browser.close()
            this = input('succeed to register one time, just cheer up')
            self.browser.close()

        except Exception as e:
            print(e)
            error = input('this is an error')
            self.write_cookies(outlook.email)
            update_the_tb(email, 'LAST_LOGIN', get_today())
            update_the_tb(email, 'COUNTRY', self.country)
            self.browser.close()

    # 接受cookie协议
    def click_cookie_button(self):
        accept_all_btn = self.browser.execute_script(
            '''return document.querySelector('tiktok-cookie-banner').shadowRoot.querySelector('button:nth-child(2)')''')
        if accept_all_btn:
            accept_all_btn.click()

    # 根据xpath点击子元素
    def click_element_based_father(self, xpath_pattern, father_dot=None):
        if father_dot:
            birth_year = father_dot.find_element(By.XPATH, xpath_pattern)
        else:
            birth_year = self.browser.find_element(By.XPATH, xpath_pattern)
        webdriver.ActionChains(self.browser).move_to_element(birth_year).perform()
        webdriver.ActionChains(self.browser).click(birth_year).perform()
        return birth_year

    # 填写birth信息
    def add_birth_infomation(self, birth_month, birth_day, birth_year):
        """
        填写 birth info
        :return:
        """
        # birth elements
        self.wait_xpath('.//div[contains(@class,"DivAgeSelector")]')
        birth_elements = self.browser.find_element(By.XPATH, './/div[contains(@class,"DivAgeSelector")]')
        # birth year
        self.click_element_based_father('//*[@id="loginContainer"]/div[1]/form/div[2]/div[3]')
        time.sleep(random.random() * 2)
        birth_year_pattern = './/div[@id="Year-options-item-%s"]' % (
                2022 - birth_year)  # % (birth_day - 1)
        self.click_element_based_father(birth_year_pattern, birth_elements)
        # birth day
        self.click_element_based_father('//*[@id="loginContainer"]/div[1]/form/div[2]/div[2]')
        time.sleep(random.random() * 2)
        birth_day_pattern = './/div[@id="Day-options-item-%s"]' % (birth_day - 1)
        self.click_element_based_father(birth_day_pattern, birth_elements)
        # birth month
        self.click_element_based_father('//*[@id="loginContainer"]/div[1]/form/div[2]/div[1]')
        time.sleep(random.random() * 2)
        birth_month_pattern = './/div[@id="Month-options-item-%s"]' % (birth_month - 1)  #
        self.click_element_based_father(birth_month_pattern, birth_elements)

    # 填写邮箱和密码
    def add_email_passwd(self, email, password):

        # passwd
        time.sleep(random.random())
        passwd_element = self.click_element_based_father('.//input[@type="password"]')
        time.sleep(random.random() * 2 + 1)
        passwd_element.send_keys(password)
        time.sleep(random.random() + 1)
        # email
        time.sleep(random.random() * 2)
        email_element = self.click_element_based_father('.//input[@name="email"]')
        time.sleep(random.random() * 3 + 2)
        email_element.send_keys(email)

    # 保存cookie,携带 email 地址
    # 保存cookie,携带 email 地址
    def write_cookies(self, email):
        this_cookies = self.browser.get_cookies()  # 获取cookies
        dumps_str = json.dumps(this_cookies, ensure_ascii=False)
        if 'csrf_session_id' in dumps_str:
            with open(os.path.join(User_Cookie_Dir, "%s.json" % email), 'w', encoding='utf-8') as f:
                f.write(dumps_str)  # 将cookies保存为json格式
                logger.info('write  cookies info to the json')
                return True
        return False

    def debug_stop(self):
        while 1:
            pass

    def wait_xpath(self, xpath_pattern, ):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    # 如果点击发送邮件出现图片验证，需要进行
    def deal_verication_code(self):
        # 发送验证码
        send_email_button = self.browser.find_element(By.XPATH, './/button[@data-e2e="send-code-button"]')
        send_email_button.click()
        time.sleep(1.5 + random.random())
        self.browser.execute_script("arguments[0].click();", send_email_button)
        time.sleep(8)

        def this_exist(xpath_pattern: str):
            try:
                return self.browser.find_element(By.XPATH, xpath_pattern)
            except:
                return False

        vericaiton_over = this_exist('.//form//div[@type="error"]/span')
        if vericaiton_over is not False:
            logger.error('Too much time try in one time')
            return False
        vericaiton_state = self.deal_verication_pic()  # 0 无验证       1  环形   2 图片拖动  3 图片相同元素验证
        if vericaiton_state != 0:
            self.deal_the_img(vericaiton_state)
            time.sleep(5)
            vericaiton_over = this_exist('.//form//div[@type="error"]/span')
            if vericaiton_over is not False:
                logger.error('Too much time try in one time')
                return False
        return True

    def deal_the_img(self, vericaiton_type):
        '''
        :param vericaiton_type:  1 双环    2 图片拖动 3  图片 同样元素
        :return:
        '''
        from utils.verication.powerddddocr import ddddOcr_tk
        from utils.verication.rotate_captcha import tk_circle_discern
        # img 外部容器
        img_outer_container = None
        this_xpath_pattern = None  # 图片 二维码 pattern
        if vericaiton_type == 1:  # 外环
            this_xpath_pattern = './/div[@class="sc-jTzLTM kuTGKN"]'
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
        elif vericaiton_type == 2:  # 图片
            this_xpath_pattern = './/div[contains(@class,"captcha_verify_img--wrapper")]'
            img_outer_container = self.browser.find_element(By.XPATH, this_xpath_pattern)
        elif vericaiton_type == 3:
            this_xpath_pattern = './/img[@id="captcha-verify-image"]'
            logger.error('this is the picture choose img???')
            input('please deal the problem by hand,input waiting...')
            return
        # 外圈图片   背景图片
        outer_pic = img_outer_container.find_element(By.XPATH, './img[1]')
        outer_pic = outer_pic.get_attribute('src')
        common_download_image(outer_pic, 'outer.png')  # 下载图片
        # 内圈图片   目标小图片
        inner_pic = img_outer_container.find_element(By.XPATH, './img[2]')
        inner_pic = inner_pic.get_attribute('src')
        # 下载到本地
        common_download_image(inner_pic, 'inner.png')  # 下载图片
        print('have download the two picture')
        # 验证码本地识别
        distance = None  # 需要拖动的距离
        if vericaiton_type:
            angle = tk_circle_discern('inner.png', 'outer.png')
            distance = angle / 180 * (340 - 64)
        else:
            distance = ddddOcr_tk('inner.png', 'outer.png')
            distance = distance * 0.62
        this_track = [int(distance // 4), int(distance // 4), int(distance * 0.3), int(distance * 0.2) + 5,
                      -8]  # 模拟鼠标拖动的点移
        this_track.append(int(distance) - sum(this_track))
        self.hold_on_slide(this_track)  # 拖动滑块 模拟移动
        self.judge_the_img_src_change(this_xpath_pattern + '/img[2]/@src', inner_pic, vericaiton_type)

    # 判断验证码是否改变， 验证成功后验证码消失，或者失败验证码refresh
    def judge_the_img_src_change(self, this_xpath_pattern, last_inner_img_url: str, circle):
        this_xpath_pattern = this_xpath_pattern  # inner_img_url pattern
        response = self.browser.page_source
        html = etree.HTML(response)
        verication = html.xpath('.//div[contains(@class,"captcha_verify_container")]')  # 验证码块
        import time
        if verication:
            img_src = html.xpath(this_xpath_pattern)  # 验证码图片
            if len(img_src) == 1 and img_src[0] != last_inner_img_url:  # 验证码已经改变
                # self.browser.implicitly_wait(5)
                print("img_src%s" % img_src)
                time.sleep(5)  # 等待 5s
                self.deal_the_img(circle)
            # 验证码没有改变 或者加载错误
            else:
                time.sleep(10)
                self.judge_the_img_src_change(this_xpath_pattern, last_inner_img_url, circle)
        else:
            print('Success to over the picture')
            self.verication_success = True  # 成功
            return True

    # 模拟滑动验证
    def hold_on_slide(self, tracks):
        import time, random
        try:
            slider = self.browser.find_element(By.XPATH, './/div[contains(@class,"secsdk-captcha-drag-icon")]')
            # 鼠标点击并按住不松
            webdriver.ActionChains(self.browser).click_and_hold(slider).perform()
            # 让鼠标随机往下移动一段距离
            webdriver.ActionChains(self.browser).move_by_offset(xoffset=0, yoffset=100).perform()
            time.sleep(0.15)
            for item in tracks:
                webdriver.ActionChains(self.browser).move_by_offset(xoffset=item,
                                                                    yoffset=random.randint(-1, 1)).perform()
                time.sleep(random.uniform(0.02, 0.15))
            # 稳定一秒再松开
            time.sleep(1)
            webdriver.ActionChains(self.browser).release().perform()
            time.sleep(1)
        except Exception as e:
            print(e)

    def deal_verication_pic(self):
        res = self.is_exist('.//div[@class="sc-jTzLTM kuTGKN"]/img[2]')
        if res:
            return 1
        res = self.is_exist('.//div[contains(@class,"captcha_verify_img--wrapper")]/img[2]')
        if res:
            return 2
        res = self.is_exist('.//img[@id="captcha-verify-image"]')
        if res:
            return 3
        return 0

    def is_exist(self, xpath_pattern) -> bool:
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait_xpath(xpath_pattern)
            return True
        except Exception as e:
            return False

    # 随机生成名称
    def random_user_name(self):
        _name = ''
        from random_word import RandomWords
        r = RandomWords()
        # Return a single random word
        _name += r.get_random_word()
        self.wait_xpath('.//input[@name="new-username"]')

        def test_name_input(input_name):
            user_name = self.click_element_based_father('.//input[@name="new-username"]')
            if user_name:
                user_name.send_keys(input_name)

        test_name_input(_name)  # 输入 word
        # 注册按钮
        while not self.judge_button_clickable('.//button[@type="submit"]'):
            random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            test_name_input(random_str)
            time.sleep(1)
        button = self.browser.find_element(By.XPATH, './/button[@type="submit"]')
        self.browser.execute_script("arguments[0].click();", button)

    def judge_button_clickable(self, xpath_pattern):
        button = self.browser.find_element(By.XPATH, xpath_pattern)
        is_disabled = button.get_attribute("disabled") is not None
        if is_disabled:
            return False
        else:
            return True
        # button_class = button.get_attribute('class')
        # logger.info('button_class_for_verication_code is {}'.format(button_class))
        # return 'disable' in button_class
        #

    def check_ip_country(self):
        self.browser.get("http://myip.ipip.net/")
        html = self.browser.page_source
        match = re.search(r"来自于：(.*?)\s{2}", html)
        if match:
            country = match.group(1)
            self.country = country

    def close_broswer(self):
        self.browser.close()
        shut_chrome_thread(self.browser_port)
