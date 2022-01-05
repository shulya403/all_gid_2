from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd

class Req(object):
    Desktop = ["Windows", "Macintosh", "Linux"]


    def __init__(self):


        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument("user-data-dir=C:\Program Files (x86)\Google\Chrome\Application\selenium")
        # options.add_argument("--remote-debugging-port=9222")

        user_agents_base = pd.read_excel("user_agents.xlsx")
        user_agents_base = user_agents_base[user_agents_base['Ok'] == 1]['User-Agents']
        self.user_agent = user_agents_base.iloc[random.randint(0, len(user_agents_base))]
        str_agent = '--user-agent="' + self.user_agent + '"'
        print(str_agent)
        options.add_argument(str_agent)

        user_screen = True
        for i in self.Desktop:
            if i in self.user_agent:
                user_screen = False
                break

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        if user_screen:
            self.driver.set_window_size(360,720)
        else:
            self.driver.set_window_size(1920,1080)


    def selenium(self, url, **kwargs):


        #driver = webdriver.Chrome(executable_path=r'C:\Users\shulya403\Shulya403_works\Ya-parse\selen\chromedriver.exe', options=options)
        try:

            self.driver.get(url)


            # self.text = self.driver.page_source

        except Exception:
            print('чет не то')

class Main(object):
    def __init__(self, page):
        self.entrance_page_url = page
        random.seed()

    def Google_Accont(self):

        # account = self.driver.find_element_by_css_selector('a.gbgt')
        account = self.request.driver.find_element_by_partial_link_text('Войт')
        if account:
            account.click()


    def Go(self):

        self.request = Req()
        self.request.selenium(self.entrance_page_url)
        self.Google_Accont()

### Go

Go = Main("https://google.ru").Go()
input()





