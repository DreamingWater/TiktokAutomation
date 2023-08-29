import json
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.common.by import By
from Browser.user_meta import RandomUserMeta
from Source.chrome.Chrome import run_chrome_thread
from tiktok_config import Working_Exe_Path, Chrome_Extension_Dir
from utils.common import horn_prompt
import re
import undetected_chromedriver as uc
from loguru import logger

class OutlookMailRegister(RandomUserMeta):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://www.outlook.com'
        self.url = 'https://www.outlook.com'
        self.login_url = 'https://login.live.com/'
        self.register_url = 'https://signup.live.com/'
        self.broswer_dir = os.path.join(os.getcwd(), 'Browser')

        # option = webdriver.ChromeOptions()
        # start_clean_plugin = os.path.join(Chrome_Extension_Dir, "extension_pooaemmkohlphkekccfajnbcokjlbehk")
        # option.add_argument(f"--load-extension=%s" % start_clean_plugin)
        # option.add_argument("--disable-blink-features=AutomationControlled")
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        # self.browser = uc.Chrome(options=option)
        # self.browser = webdriver.Chrome(options=option)
        # with open(os.path.join(Working_Exe_Path, 'Browser', 'storage', 'stealth.min.js')) as f:
        #     js = f.read()
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })

        self.browser_port = 9223
        run_chrome_thread(self.browser_port)
        time.sleep(5)
        # 启用带插件的浏览器

        option = webdriver.ChromeOptions()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:%s" % self.browser_port)
        chrome_driver_path = os.path.join(self.broswer_dir, "chromedriver.exe")
        self.browser = webdriver.Chrome(executable_path=chrome_driver_path, options=option)

        self.wait = WebDriverWait(self.browser, 10)
        self.verication_success = False

    # 启动 clean 插件
    def click_clean_button_crt(self):
        pass
        time.sleep(5)
        self.wait_xpath('.//img[@class="inserted-btn mtz"]')
        clean_button = self.browser.find_element(By.XPATH, './/img[@class="inserted-btn mtz"]')
        clean_button.click()

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

    def judge_element_success_or_not(self, xpath_pattern, error_hander):
        """
        判断邮箱是否可用, 可用返回password输入元素，否则从新开始邮箱输入
        :return 密码输入定位元素:
        """
        password_input = self.is_exist(xpath_pattern)  # 密码输入框
        if not password_input:  # 没找到密码输入框
            print('can not find the the element: {}'.format(xpath_pattern))
            error_hander()  # 重新填写邮箱表单
        else:  # 找到密码输入框
            return password_input

    def input_email_in_register(self):
        # 获取邮箱和密码
        self.request_user_meta()
        # 邮箱名称
        self.send_key_to_element('.//input[@id="MemberName"]', self.email)  # 填写邮箱
        # 提交按钮
        self.sumbit_button_click('.//input[@type="submit"]')
        time.sleep(5)  # 隐式等待
        # 判断邮箱是否可用,可用返回password输入元素，否则重新获取meta中的邮箱
        password_input = self.judge_element_success_or_not('.//input[@id="PasswordInput"]',
                                                           self.input_email_in_register)
        # 输入 密码，并确认
        password_input.send_keys(self.password)
        time.sleep(5)
        self.sumbit_button_click('.//input[@type="submit"]')

    def check_phone_number_need(self):
        res = self.is_exist('.//input[contains(@id,"PhoneInput")]')
        if res:
            res.send_keys('17830373031')
            self.sumbit_button_click('.//a[@role="button"]')
            input('Phone number is needed!')
            self.save_user_data()
            logger.error('Outlook register need email, so give up')
            return True
        return False

    # 注册 register
    def register(self):
        self.browser.get(self.register_url)  # 注册页面
        self.browser.maximize_window()
        self.click_clean_button_crt()
        self.browser.refresh()
        self.sumbit_button_click('.//input[@type="submit"]')  # 同意并退出
        time.sleep(5)
        self.input_email_in_register()
        # 输入姓名和出生信息
        self.add_user_infomation(self.firstname, self.lastname)
        # 是否需要处理手机号
        res = self.check_phone_number_need()
        if res:
            self.save_user_data()
            return False
        # 验证码 授权
        from loguru import logger
        logger.info(self.email, self.password)
        self.verication_right()

        # 储存用户数据
        self.save_user_data()
        self.browser.close()
        return True

    def send_key_to_element(self, xpath_pattern, keys):
        self.wait_xpath(xpath_pattern)  # 等待元素加载
        member_name = self.browser.find_element(By.XPATH, xpath_pattern)  # 找到元素
        member_name.send_keys(keys)

    def wait_xpath(self, xpath_pattern, ):
        element = (By.XPATH, xpath_pattern)
        self.wait.until(EC.presence_of_element_located(element))

    def sumbit_button_click(self, xpath_pattern):
        self.wait_xpath(xpath_pattern)  # 等待按钮加载完毕
        submit_button = self.browser.find_element(By.XPATH, xpath_pattern)  # 按钮
        self.browser.execute_script("arguments[0].click();", submit_button)

    def add_user_infomation(self, first_name: str, last_name: str):
        # 判断是否可以，输入姓名
        last_name_element = self.judge_element_success_or_not('.//input[@id="LastName"]',
                                                              self.input_email_in_register)
        last_name_element.send_keys(first_name)  # 姓
        first_name_element = self.browser.find_element(By.XPATH, './/input[@id="FirstName"]')
        first_name_element.send_keys(last_name)  # 名
        time.sleep(3)
        self.sumbit_button_click('.//input[@type="submit"]')
        time.sleep(3)
        # 输入出生地址
        # 输入 年 月 日
        # birth_month_pattern.
        time.sleep(1)
        # birth_day
        birth_data_pattern = './/select[contains(@class,"datepart2")]/option[%s]' % self.birth_month
        self.wait_xpath(birth_data_pattern)
        self.browser.find_element(By.XPATH, birth_data_pattern).click()

        # birth_month
        birth_month_pattern = './/select[contains(@class,"datepart1")]/option[%s]' % self.birth_month
        self.wait_xpath(birth_month_pattern)
        self.browser.find_element(By.XPATH, birth_month_pattern).click()

        # birth_year
        self.wait_xpath('.//input[@type="number"]')
        birth_year_element = self.browser.find_element(By.XPATH, '//input[@type="number"]')
        birth_year_element.send_keys(self.birth_year)




        self.sumbit_button_click('.//input[@type="submit"]')  # 确定

    # verication_right 验证和授权
    def verication_right(self):
        # 下一步按钮
        # try:
        #     button_pattern = './/button[contains(@class,"button")]'
        #     button_element = (By.XPATH, button_pattern)
        #     WebDriverWait(self.browser, 60).until(EC.presence_of_element_located(button_element))
        #     self.browser.find_element(By.XPATH, './/button[contains(@class,"button")]').click()
        # except Exception as e:
        #     pass
        # 喇叭提示用户控制
        # horn_prompt()
        # 验证码
        self.deal_pic_verication()
        # 拒绝许可协议
        self.reject_long_session()
        # 等待知道成功加载,
        self.succeed_to_register()
        # 关闭页面
        # self.browser.close()

    # 等待知道页面成功加载
    def succeed_to_register(self):
        self.browser.implicitly_wait(20)  # 隐式等待
        # EgoYiBQzuMD9@outlook.com q9ox@5jPmF7o5
        while 'login' in self.browser.current_url: pass

    def get_email_content(self, xpath_pattern):
        self.wait_xpath(xpath_pattern)
        email_datas = self.browser.find_elements(By.XPATH, xpath_pattern)
        # 从 the_last_email_data 元素的 aria-label 属性中提取验证码
        for email_data in email_datas:
            try:
                aria_label = email_data.get_attribute('aria-label')
                print('aria_label is {}'.format(aria_label))
                if aria_label and 'TikTok' in aria_label:
                    result = re.search(r'\b(\d{6})\b', aria_label)
                    if result:
                        code = result.group(1)
                        return code
            except:
                ...
        return False

    def find_the_tk_email(self):
        # 访问邮箱页面
        current_url = self.browser.current_url
        self.browser.get('https://outlook.live.com/mail/0/')
        if current_url == self.browser.current_url: self.browser.refresh()  # 刷新页面
        self.browser.implicitly_wait(5)
        # 获取最新的email
        the_last_email_pattern = './/div[@class="zXLz3 EbLVy"]/div'
        # 重点的email内容
        email_content = self.get_email_content(the_last_email_pattern)
        if email_content is not False:
            return email_content
        # 其它的email内容
        self.check_others_box()
        email_content = self.get_email_content(the_last_email_pattern)
        return email_content

    def check_others_box(self):
        self.wait_xpath('.//button[@name="其他"]')
        button_other = self.browser.find_element(By.XPATH, './/button[@name="其他"]')
        self.browser.execute_script("arguments[0].click();", button_other)
        self.browser.implicitly_wait(10)

    # 处理 图片验证码
    def deal_pic_verication(self):
        try:
            self.deal_notice_page() # 等待 Btn Button 或者 登录
        except:
            self.deal_pic_verication()

    # 最新的问题是 隐私页面错误
    def deal_notice_page(self):
        if 'privacynotice' in self.browser.current_url:
            logger.info('the email and passwd is {}:{}'.format(self.email,self.password))
            login_url = "https://login.live.com/login.srf"
            self.browser.get(login_url)
            return True
        else:
            # 继续等待 idBtn
            self.wait_xpath('.//input[@id="idBtn_Back"]')
            self.browser.find_element(By.XPATH, './/input[@id="idBtn_Back"]')

    # 拒绝持久登录协议
    def reject_long_session(self):
        id_btn_back = self.browser.find_element(By.XPATH, './/input[@id="idBtn_Back"]')  # 否
        self.browser.execute_script("arguments[0].click();", id_btn_back)

    def get_outlook_website(self)->bool:
        # 测试ip
        self.check_ip_country()
        # if '北京' in self.country:
        #     raise "the ip is not right..."
        # 注册
        return self.register()

    def debug_stop(self):
        while 1:
            pass

    def check_ip_country(self):
        self.browser.get("http://myip.ipip.net/")
        html = self.browser.page_source
        match = re.search(r"来自于：(.*?)\s{2}", html)
        if match:
            country = match.group(1)
            self.country = country
