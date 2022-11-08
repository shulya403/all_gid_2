from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd

from pywinauto.application import Application
import pywinauto.findwindows as pywin_find


class Cookies(object):
    def __init__(self, id=0):
        if id == 0:
            self.current_cookies = {
                "host": "yandex.ru",
                "cookies": {
                    "is_gdpr": 0,
                    "is_gdpr_b": "CIbRLhCZdCg",
                    "mda": 0,
                    "yandex_gid": 213,
                    "yandexuid": 8565281421653142005,
                    "yuidss": 8565281421653142005,
                    "my": "YwA=",
                    "i": "IvsRsbG/CuCr2mb9rfz22cUVx7AXiq9irA3jJ08m6hjGm5YI058c29E3dghFbO6PJudymgSl/K/iMHhOvJIqp9qvhTU=",
                    "ymex": "1968502006.yrts.1653142006#1968502006.yrtsi.1653142006",
                    "gdpr": 0,
                    "_ym_isad": 2,
                    "_ym_uid": 1653142007124738218,
                    "_yasc": "7xG+PyHV95d+jZBx62H1h/izIgosVDP45Oyoy50b8YDGGzXxLGaiLsstXbrG6qjVIDQ=",
                    "_ym_d": 1653142121,
                    "yabs-frequency": "/5/0G00013oY6800000/rhWDDgwQt5oiHY5ZIlIyL2gUUAn68F1Zk3nQjSnbh4OXjPHRF5jnOroiHYCYxKy43AJ6Rgn68m00/",
                    "skid": 2387906501653142123,
                    "ys": "wprid.1653142160905383-8927943903178425581-sas6-5255-1e3-sas-l7-balancer-8080-BAL-5790",
                    "yp": "1655734006.ygu.1#1668910009.szm.1:1920x1080:1823x964#1653314812.gpauto.55_719036:37_727497:1853:0:1653142002#1655820530.csc.1#1684678033.p_sw.1653142033#1653746833.mcv.1#1653746962.mcl.#1653228562.ln_tp.01",
                    "lsq": "мой ip",
                }
            }
        elif id == 1:
            self.current_cookies = {
                "host": "yandex.ru",
                "cookies": {
                    "is_gdpr_b": "COuhXRDjHSgC",
                    "fuid01": "60ac418c0cb18956.g03t1YJqU9uG75GVmqcboEQc6H2w7wPe7SXFG9cTu1bTe1qQPzazmC2MAFQ8c38kmRw_6cyyF84hPZiqAF70gSrCd4PXWRf_bh0M0UBpoJ5yqEPKHptOC8MwXtofa_DV",
                    "font_loaded": "YSv1",
                    "yandex_login": "dmschulgin",
                    "amcuid": "1084130751644361937",
                    "L": "Vld1dwB7TUN0dnABXAxgBEd8cHcAQUcBNiQ5FSsUOwkdVw == .1646506346.14907.328256.3da08424f397c106d755732e4ca9e3f5",
                    "my": "YycCAAMA",
                    "yandexuid": 7149064641575729573,
                    "_ym_uid": 1575729574981578479,
                    "gdpr": 0,
                    "yandex_gid@": 213,
                    "is_gdpr": 0,
                    "yuidss": 7149064641575729573,
                    "ymex": "1963426423.yrts.1648066423# 1937333617.yrtsi.1621973617",
                    "mda": 0,
                    "bltsr": 1,
                    "KIykI": 1,
                    "instruction": 1,
                    "i": "LW9dmMOHl5aCsbnrhQA4hGwc7bBz64YyF0iJGf4JQY/oFFkRwX9sW9lvMidfFcitLKmI9n4o78I8CCk6By2YQ/OsJUc=",
                    "Session_id": "3:1652992113.5.0.1639889370196:UeY3F-B8VhzIACCBcBMAKg:29.1.2:1|919128238.6616976.2.2:6616976|3:252587.843137.***",
                    "sessionid2": "3:1652992113.5.0.1639889370196:UeY3F-B8VhzIACCBcBMAKg:29.1.2:1.499:1|919128238.6616976.2.2:6616976|3:252587.740842.***",
                    "yabs-frequency": "/5/001E0W00001NrOXY/Qmq8nK8OTcIiHY22NQdjx4NyKAn6GErasi8hrRnNh4PWLNC5EbYSntciHa1Mv5Okcw6rMgr6004Tpdkb4MhpVQn6G4dt6DPUIJ5shKQW0j9LGSKxW_Duh4OWIdkmS9K0002iHY05LB1mbG000An684bxi72L0000h4Q0O-2FhFPgncciHY3zlprY9w0GHAn688Pa6JjNZ_Hdh4PWpJPUu2hG5bYiHi3S1vvs1ygfSwn6O5FgNBbbKZbzh4OWW94KqVuuxsAiHY2NJpAM9XekIgr6u047Lh1mbG000An6e29wi72L0000h4P00ssmS9K0002iHY0KLh1mbG000An6GCoU052X8TP7hKR00JHbwF0zNqz1hKRW1EnWzgdOFXDwh4QWs7EmS9K0002iHe0r17Dmb0000An68FtvSd2K0000h4OWMmPpS9G0002iHY0G_d9mb0000An6GFxvSd2K0000h4PWUrMmS9K0002iHc283nnmaW000An68BCR772I0000h4OWjHiSS980002iHY3x4XnmaW000An6GFjKi72L0000hKR01BzPi72L0000h4PWEWPpS9G0002iHY1lUB1mbG000An6GEvti72L0000h4R0idQmS9K0002iHY3hLB1m00000An68000/",
                    "_ym_isad": 1,
                    "SL_G_WPT_TO": "ru",
                    "SL_GWPT_Show_Hide_tmp": 1,
                    "SL_wptGlobTipTmp": 1,
                    "_yasc": "ITp8WER3KBTML18JjAY4U3j+eu3re3PJsiSzlpJfEQgp2hn3ziWOdXHBAh5UN+a1X8ZyYoDapSfmsg==",
                    "yp": "1682799287.p_sw.1651263287#1667682686.p_cl.1636146686#1668172663.szm.1:1920x1080:1823x977#1931112193.multib.1#1935593002.ygp.2#1657542972.stltp.serp_bk-map_1_1626006972#1661451851.mco.01#1655408969.csc.2#1653805362.sz.640x360x3#1961866346.udn.cDrQlNC80LjRgtGA0LjQuSDQqNGD0LvRjNCz0LjQvQ==#1963426340.pcs.0#1653854728.spcs.l#1653349033.mcv.0#1653349033.mcl.1jtu26l#1653400430.clh.2353491-306",
                    "lsq": "мой ip",
                    "ys": "startextchrome.Commertial#.#wprid.1653142306680769-5337273116591677763-sas2-0341-sas-l7-balancer-8080-BAL-9835"
                }
            }


# options = webdriver.ChromeOptions()
# # Например для симуляции браузера Android QQ
# #options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
# #options.add_argument("user-data-dir=C:\Program Files (x86)\Google\Chrome\Application\selenium")
#
# #driver = webdriver.Chrome(executable_path=r'C:\Users\shulya403\Shulya403_works\Ya-parse\selen\chromedriver.exe', options=options)
# #C:\Users\shulya403\Shulya403_works\Ya-parse\selen\chromedriver.exe
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# #cookie = Cookies(id=1)
#
# #domain = cookie.current_cookies["host"]
#
# driver.get("https://zen.yandex.ru/media/id/60a9bdd6a4aad1743d7ea041/igrovye-monitory-bestsellery-za-dekabr-2021-620bae452564a00e79335a34")
# time.sleep(1)
# a = driver.find_element_by_link_text("Игровые мониторы: Top-10, в декабре `21")
# a.location_once_scrolled_into_view
# time.sleep(2)
# #a.click()
# driver.execute_script("arguments[0].click();", a)

# for k,v in cookie.current_cookies["cookies"].items():
#     print(k, v)
#     driver.add_cookie({"name": k, "value": str(v)})
# driver.refresh()
#input()

class Crowl_To_Buildlinks(object):
    def __init__(self,
                 file_user_agents = "user_agents.xlsx",
                 file_bulild_links = "build_links.xlsx"):

        self.list_build_links = self.Get_Build_Links(file_bulild_links)
        self.list_user_agents = self.Get_User_Agents(file_user_agents)

        random.seed()

    def Get_Build_Links(self, filename):

        df_ = pd.read_excel(filename)
        list_exit = df_[df_['Ok'] == 1]['Href'].to_list()

        return list_exit

    def Get_User_Agents(self, filename):

        df_ = pd.read_excel(filename)
        list_exit = df_[df_['Ok'] == 1]['User-Agents'].to_list()

        return list_exit

    def Proxie_try(self, site, proxie_base="https://hidemy.name/ru/proxy-list/?country=BYKZLVRUUAUZ#list"):

        options = webdriver.ChromeOptions ()
        # options.add_argument(user_agent)
        options.add_argument ('--disable-gpu')
        # options.add_argument("--headless")

        if self.proxie_list_actual:
            pass
        else:
            try:
                driver_proxie_base = webdriver.Chrome (ChromeDriverManager ().install (), options=options)
                #driver_proxie_base.set_window_size (1920, 1080)
                driver_proxie_base.get (proxie_base)
                tbl_on_proxie_page = pd.read_html (driver_proxie_base.page_source)
                proxy_table = tbl_on_proxie_page[0]
                proxy_table = proxy_table[proxy_table['Тип'] != 'HTTP']
                print (proxy_table)
                for i, row in proxy_table.iterrows ():
                    self.proxie_list_actual.append(row['Тип'].lower () + "://" + str(row['IP адрес']) + ":" + str(row['Порт']))
                driver_proxie_base.quit ()

            except Exception as Err:
                print (Err)
                self.proxie_list_actual = []
                return ""

        while self.proxie_list_actual:
            this = random.randint (0, len (self.proxie_list_actual) - 1)
            print ("Проверка прокси: {}".format (self.proxie_list_actual[this]))
            options.add_argument("--proxy-server=%s" % self.proxie_list_actual[this])

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            try:
                driver.get(site)
                wait = WebDriverWait(driver, 5).until(EC.c)
                print ("OK прокси ->", self.proxie_list_actual[this])
                driver.quit()
                return self.proxie_list_actual[this]
            except Exception:
                print ("битый прокси", self.proxie_list_actual.pop (this))
                print (len (self.proxie_list_actual))
                driver.quit()

        return ""

    def Selenium_Window(self, user_agent=False, proxy=False, cookies=False, proxie_list_actual=[], list_profile=['Default']):

        options = webdriver.ChromeOptions ()

        if proxy:
            self.proxie = True
            self.proxie_list_actual = proxie_list_actual
            choiced_proxie = self.Proxie_try(site='https://allgid.ru')
            if choiced_proxie:
                proxie = "--proxy-server=" + choiced_proxie
                options.add_argument(proxie)

        if user_agent:
            random_user_agent = self.list_user_agents[random.randint(0, len(self.list_user_agents)-1)]
            options.add_argument('user-agent=' + "\"" + random_user_agent + "\"")

            print(random_user_agent)
            # if ("Windows" or "Linux" or "Macintosh") in random_user_agent:
            #    options.add_argument('window-size=1920,1080')
            # else:
            #    options.add_argument('window-size=420,1080')

        options.add_argument('disable-infobars')

        options.add_argument (r'user-data-dir=C:\Users\shulya403\AppData\Local\Google\Chrome\User Data')

        #list_profile=['Default', 'Profile 3']
        this_profile=list_profile[random.randint(0, len(list_profile) - 1)]
        print(this_profile)
        profile_dir = r'--profile-directory=' + this_profile

        options.add_argument(profile_dir)

        #driver = webdriver.Chrome(ChromeDriverManager ().install(), options=options)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        print("connection...")

        return driver

    def Go_Scrape(self, url_ = "", speed_lag=25, allgid_dept=2, q=10, q_lag=620, user_agent=False):

        if not url_:
            referer_url = self.list_build_links[random.randint(0, len(self.list_build_links)-1)]
        else:
            referer_url = url_

        driver = self.Selenium_Window(user_agent=user_agent)

        try:
            driver.get(referer_url)
        except Exception as Err:
            print(Err)
            pass

        print("Зашли: ", referer_url)
        time.sleep(2)
        page_links = driver.find_elements_by_tag_name('a')

        random_allgid_link = self.Get_Allgid_Link(page_links)

        if random_allgid_link:
            time.sleep(random.randint(0, 5))

            random_allgid_link.location_once_scrolled_into_view
            time.sleep(2)
            try:
                random_allgid_link.click()
            except Exception:
                driver.execute_script("arguments[0].click();", random_allgid_link)

            for i in range(1, random.randint(2,allgid_dept)):
                print("идем на allgid раз: ", i)
                self.Crowl_allgid(driver, speed_lag)
        driver.quit()
        print("ждем ", q_lag, ">>>", end="")
        for i in range(q_lag):
            time.sleep(1)
            print(".", end="")
            if (i > 1) and (i % 100) == 0:
                print("\n")

    def Crowl_allgid(self, driver, speed_lag):


        time.sleep(random.randint(2, speed_lag))

        windows_q = len(driver.window_handles)
        #print(windows_q)
        if windows_q > 1:
            driver.switch_to.window(driver.window_handles[windows_q-1])

        page_links = driver.find_elements_by_tag_name('a')

        start_moving = 3

        #Гуляем по странице
        while start_moving < len(page_links) - 5:
            lnk_num = start_moving + random.randint(1, 5)
            try:
                page_links[lnk_num].location_once_scrolled_into_view
                click_prob = int(random.expovariate(0.4))
                #print(lnk_num, page_links[lnk_num].text,  click_prob )
                if click_prob == 2:
                    if "https://allgid.ru" in page_links[lnk_num].get_attribute('href'):
                        try:
                            page_links[lnk_num].click()
                        except Exception:
                            try:
                                driver.execute_script("arguments[0].click();", page_links[lnk_num])
                            except Exception:
                                pass
                        break

            except KeyError:
                pass
            time.sleep(random.randint(0, 2))

            start_moving = lnk_num

    def Get_Allgid_Link(self, page_links):
        if page_links:
            try:
                allgid_page_links = list ()
                for lnk in page_links:
                    lnk_href = lnk.get_attribute ('href')
                    if lnk_href:
                        if "allgid" in lnk_href:
                            allgid_page_links.append (lnk)
                # allgid_page_links = [lnk for lnk in page_links if 'allgid.ru' in lnk.get_attribute('href')]

                print ("Ссылок на allgid: ", len (allgid_page_links))

                random_allgid_link = allgid_page_links[random.randint (0, len (allgid_page_links) - 1)]
                random_allgid_url = random_allgid_link.get_attribute ('href')

                print ("URL allgid: ", random_allgid_url)
            except Exception:

                random_allgid_link = page_links[0]
            finally:
                return random_allgid_link

        else:
            print ("чет нето")
            return None

class WinChrome(object):
    def __init__(self, list_profile = ['Default'], browser="chrome"):
        self.browser = browser
        self.list_profile = list_profile


        if self.browser == "chrome":
            app = Application(backend="uia").start ("C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility")
            #app = Application(backend="uia").start ("notepad.exe")
            bro_root = app.Pain
            app.wait_cpu_usage_lower()
            bro_root.wait('ready', timeout=10)

            app[r"Кто использует Chrome?"].print_control_identifiers()

            bro_root.Button1.click()
            #app.Pane.Pane2.click()

            # # wait till the window is really open
            # actionable_dlg = dlg_spec.wait('visible')
        elif self.browser == "firefox":
            app = Application(backend="uia").start("C:\Firefox\X-Firefox.exe")
            app.wait_cpu_usage_lower ()
            bro_root = app[r"Starting page — Mozilla Firefox"]

            #bro_root.wait('ready', timeout=10)
            bro_root.print_control_identifiers()

#win = pywin_find.enum_windows()

#CromeWindwow = WinChrome(browser="firefox")


Scraper = Crowl_To_Buildlinks()

count = 0
for i in range(300):
    q_lag=random.randint(3, 20)
    print(">>>>>> ЗАХОД > ", i, q_lag)
    #Scraper.Go_Scrape(allgid_dept=20, q_lag=q_lag, user_agent=False)
    driver = Scraper.Selenium_Window(proxy=False, user_agent=False, list_profile=['Profile 1'])

    try:
        driver.get("https://allgid.ru/Nb/")
    except Exception as Err:
        print(Err)
        pass
    count = count + 1
    print(count)
    for i1 in range(1, random.randint(1, 7)):
            Scraper.Crowl_allgid(driver, q_lag)
            count = count + 1
            print("allgid count >>", count)

    driver.quit()


