from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import time

TEL = "19935324869"
PASS = "aptx4869+jyw"
BORDER = 6
INIT_LEFT = 60


class CrackDouYu:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
        self.url = "https://www.douyu.com/"
        self.browser = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.tel = TEL
        self.password = PASS

    def click_login(self):
        """
        点开登陆的界面，再点击账号密码登陆
        然后再输入账号密码后弹出点击登陆后就有滑块验证码的窗口出来了
        :return:
        """
        self.browser.get(self.url)
        button_login = self.wait.until(EC.element_to_be_clickable((By.XPATH, r'//a[@class="u-login fl"]')))
        button_login.click()
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, r'//iframe[@id="login-passport-frame"]')))
        self.browser.switch_to.frame(iframe)
        button_loginbypassword = self.wait.until(EC.element_to_be_clickable((By.XPATH, r'//div[@class="scanicon-toLogin js-qrcode-switch"]')))
        print(button_loginbypassword)
        button_loginbypassword.click()
        # button = self.wait.until(EC.element_to_be_clickable((By.XPATH, r'//span[@class="geetest_radar_tip_content"]')))
        # button.click()
        count = self.wait.until(EC.element_to_be_clickable((By.XPATH, r'//input[@name="phoneNum"]')))
        count.send_keys(self.tel)
        password = self.wait.until(EC.element_to_be_clickable((By.XPATH, r'//input[@name="password"]')))
        password.send_keys(self.password)
        time.sleep(5)
        password.send_keys(Keys.ENTER)


    def get_screenshot(self):
        """
        用来截取当前浏览器的图片的。
        :return:
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_position(self):
        """
        获取验证码的位置
        :return:
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_bg geetest_absolute")))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right


    def get_slide_button(self):
        """
        获取滑块对象
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_slider_button")))
        return button


    def get_slide_image(self, name="slideImg.png"):
        """
        获取没有缺口的图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print("验证码的位置", top, bottom, left, right)
        screenshot = self.get_screenshot()
        slideImg = screenshot.crop((1.25 * top, 1.25 * bottom, 1.25 * left, 1.25 * right))
        slideImg.save(name)
        return slideImg

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1:
        :param img2:
        :param x:
        :param y:
        :return:
        """
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False


    def get_gap(self, img1, img2):
        """
        获取缺口的偏移量
        :param img1:
        :param img2:
        :return:
        """
        left = 60
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    return i
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        使用动作链，拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        self.click_login()
        img1 = self.get_slide_image("img1.png")
        slider = self.get_slide_button()
        slider.click()
        img2 = self.get_slide_image("img2.png")
        gap = self.get_gap(img1, img2)
        print("缺口位置", gap)
        gap -= BORDER
        track = self.get_track(gap)
        print('滑动轨迹', track)

        self.move_to_gap(slider, track)

        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)

        # 失败后重试
        if not success:
            self.crack()
        else:
            print("成功")

c = CrackDouYu()
c.crack()





