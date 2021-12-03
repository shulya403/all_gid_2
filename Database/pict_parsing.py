import pandas as pd
import sqlalchemy as sql
import os
#from django.conf import settings

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TODO: Подрубить названия файла xls (с ценами) с именами и ссылями на yama,
#   Последовательно идти по базе моделей
#   Если такого файла нет в static/pict
#   искать эти имена в файле, запускать URL в Selenium
#   Искать картинку и ее src на странице
#   Скачивать и записывать src через retrive

class Parse_pict(object):
    def __init__(self, cat_, links_file, work_dir = "../Data/cat_/"):

        #print(settings.BASE_DIR)
        if cat_ in ['Nb', 'Mnt', 'Ups', 'Mfp']:

            self.cat = cat_.lower()

        # DB Tables name
            self.db_products = self.cat + '_products'

        # SQL Coonection

            sql_engine = sql.create_engine("mysql://shulya403:1qazxsw2@localhost/all_gid_2?charset=utf8mb4",
                                           echo=True,
                                           encoding='utf8',
                                           convert_unicode=True)
            if sql_engine:
                self.metadata = sql.MetaData(sql_engine)
                self.connection = sql_engine.connect()
            else:
                print("чет с SQL-сервером (((")
                raise
        # links_file
        self.work_dir = work_dir.replace('cat_', self.cat.title())
        self.links_file = self.work_dir + links_file

        self.df_links = self.Df_Handle(pd.read_excel(self.links_file))

        self.Get_Db_Names()

        self.cat_static_dir = "../marketability/static/marketability/pict/" + self.cat.title() + "/"



    def Df_Handle(self, df_links_source):

        try:
            df_exit = df_links_source[df_links_source['Site'] == 'yama']
        except Exception:
            print("чет с полями в файле")
            raise

        return df_exit

    def Get_Db_Names(self):

        tbl_products = sql.Table(self.db_products, self.metadata, autoload=True)

        try:
            self.df_names = pd.read_sql(tbl_products.select(), self.connection)[['brand', 'name']]
        except Exception:
           print("чет с базой")
           raise

    def Set_pict_name(self, row):

        return row['brand'].lower() + "_" + row['name'].lower().replace(" ", "_")

    def Search_exist_pict(self, pict_name):

        if pict_name in os.listdir(self.cat_static_dir):
            return True
        else:
            return False

#  MAIN

Cat = Parse_pict("Nb", "Ноутбук-Concat_Prices--Sep-21--Checked.xlsx")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def Get_Image_TAG(driver, url_):
    driver.get(url_list[0])
    pg_title = driver.find_element_by_tag_name("title")
    print(pg_title.text)

    if not "Ой!" in pg_title.text:
        img_tag = driver.find_element_by_class_name("page")
        return img_tag.get_attr("src")
    else:
        return Get_Image_TAG(url_)

if not Cat.df_names.empty:
    for i, row in Cat.df_names.iterrows():
        image_name = Cat.Set_pict_name(row)
        print(image_name)
        url_list = Cat.df_links[Cat.df_links['Name'] == row['name']]['Modification_href'].to_list()
        if url_list:
            Get_Image_TAG(driver, url_list[0])


            input()

driver.close()









#Ноутбук-Concat_Prices--Sep-21--Checked.xlsx