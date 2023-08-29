import json
import re
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.by import By
from Browser.user_meta import RandomUserMeta
from tiktok_config import Chrome_Extension_Dir, Data_Storage_storage_Dir, Error_Html_Dir
from utils.common import horn_prompt
from loguru import logger


class OutlookMailLogin:
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.outlook.com'
        self.email_url = 'https://outlook.live.com/mail/0/'
        self.login_url = 'https://www.outlook.com/login'
        self.email = None
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')
        option = webdriver.ChromeOptions()
        start_clean_plugin = os.path.join(Chrome_Extension_Dir, "extension_pooaemmkohlphkekccfajnbcokjlbehk")
        # option.add_argument(f"--load-extension=%s" % start_clean_plugin)
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=option)
        self.wait = WebDriverWait(self.browser, 10)

    def is_exist(self, xpath_pattern):
        """
        driver.find_element(*locator)
        :param xpath_pattern:
        :return False or the Element:
        """
        try:
            self.wait_xpath(xpath_pattern)
            element = self.browser.find_element(By.XPATH, xpath_pattern)
            return element
        except:
            return False

    def input_email(self, this_email: str):
        # 页面等待加载
        self.wait_xpath('.//input[@type="email"]')
        # 邮箱名称
        self.send_key_to_element('.//input[@type="email"]', this_email)  # 填写邮箱
        self.email = this_email
        # 提交按钮
        self.sumbit_button_click('.//input[@type="submit"]')

    def input_password(self, _password: str):
        # 页面加载
        self.wait_xpath('.//input[@type="password"]')
        # 输入密码
        self.send_key_to_element('.//input[@type="password"]', _password)  # 填写邮箱
        # input('输入密码')
        # 提交按钮
        self.sumbit_button_click('.//input[@type="submit"]')

    def skip_the_back_email(self):
        time.sleep(5)
        skip_email = self.is_exist('.//a[@id="iShowSkip"]')
        if skip_email:
            self.browser.execute_script("arguments[0].click();", skip_email)

    def login(self, email: str, password: str):
        # 登录页面
        self.browser.get(self.login_url)
        # 邮箱
        self.input_email(email)
        # 密码
        self.input_password(password)
        # 如果有back_email就跳过
        self.skip_the_back_email()
        # 拒绝持久登录
        self.reject_long_session()
        # 拒绝了解更多内容
        self.shutdown_learn_more()
        # 拒绝特色登录
        self.refuse_special_login()
        logger.info('success to login the email:{}'.format(email))

    # 拒绝持久登录协议
    def reject_long_session(self):
        try:
            time.sleep(5)
            id_btn_back = self.browser.find_element(By.XPATH, './/input[@id="idBtn_Back"]')  # 否
            self.browser.execute_script("arguments[0].click();", id_btn_back)
        except:
            pass

    # 拒绝特色登录
    def refuse_special_login(self):
        refuse_login = self.is_exist('.//a[@id="iCancel"]')
        if refuse_login:
            self.browser.execute_script("arguments[0].click();", refuse_login)

    # 关闭了解更多内容
    def shutdown_learn_more(self):
        try:
            time.sleep(5)
            self.wait_xpath('.//a[@href="#/LearnMore"]')
            self.sumbit_button_click('.//input[@type="submit"]')
        except:
            pass

    def get_email_content(self, xpath_pattern):
        self.wait_xpath(xpath_pattern)
        email_datas = self.browser.find_elements(By.XPATH, xpath_pattern)
        # 从 the_last_email_data 元素的 aria-label 属性中提取验证码
        for email_data in email_datas:
            try:
                aria_label = email_data.get_attribute('aria-label')
                if aria_label and 'TikTok' in aria_label:
                    result = re.search(r'\b(\d{6})\b', aria_label)
                    if result:
                        code = result.group(1)
                        logger.info('the tiktok code is: {}'.format(code))
                        return code
            except Exception as e:
                ...
        return False

    def find_the_tk_email(self):
        try:
            # 访问邮箱页面
            current_url = self.browser.current_url
            self.browser.get('https://outlook.live.com/mail/0/')
            if current_url == self.browser.current_url: self.browser.refresh()  # 刷新页面
            self.browser.implicitly_wait(5)
            # 获取最新的email  './/select[contains(@class,"datepart1")]/option[%s]'
            the_last_email_pattern = './/div[contains(@class,"zXLz3")]/div'
            # 重点的email内容
            email_content = self.get_email_content(the_last_email_pattern)
            if email_content is not False:
                return email_content
            # 其它的email内容
            self.check_others_box()
            email_content = self.get_email_content(the_last_email_pattern)
            return email_content
        except Exception as e:
            logger.error(e)
            html = self.browser.page_source
            with open(os.path.join(Error_Html_Dir, '%s.html' % self.email), 'w', encoding='utf-8') as f:  # 保存此时的页面
                f.write(html)
            return False

    def check_others_box(self):
        self.wait_xpath('.//button[@name="其他"]')
        button_other = self.browser.find_element(By.XPATH, './/button[@name="其他"]')
        self.browser.execute_script("arguments[0].click();", button_other)
        self.browser.implicitly_wait(10)

    def send_key_to_element(self, xpath_pattern, keys):
        time.sleep(5)
        self.wait_xpath(xpath_pattern)  # 等待元素加载
        member_name = self.browser.find_element(By.XPATH, xpath_pattern)  # 找到元素
        webdriver.ActionChains(self.browser).move_to_element(member_name).perform()
        webdriver.ActionChains(self.browser).click(member_name).perform()
        member_name.send_keys(keys)

    def wait_xpath(self, xpath_pattern):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    def sumbit_button_click(self, xpath_pattern):
        self.wait_xpath(xpath_pattern)  # 等待按钮加载完毕
        submit_button = self.browser.find_element(By.XPATH, xpath_pattern)  # 按钮
        self.browser.execute_script("arguments[0].click();", submit_button)

    # 等待知道页面成功加载
    def succeed_to_register(self):
        self.wait_xpath('.//div[@class="zXLz3 EbLVy"]')

    def debug_stop(self):
        while 1:
            pass
