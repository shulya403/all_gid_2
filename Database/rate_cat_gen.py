import pandas as pd
import sqlalchemy as sql
import json
import time
import datetime as dt
from datetime import timedelta

# "Premium": {
#     "cl_gl_name": "премиальные ноутбуки",
#     "header": "Рейтинг популярности флагманских ноутбуков",
#     "cat_description": "<p>К флагманским моделям мы относим ноутбуки премиальных серий. Это высококачественные модели выделенных брендовых серий. Мы не включаем в этот перечень специализированных топовых игровых серий и мобильные рабочие станции.</p> <p>Согласно базовому позиционированию производителей, часто существует условное разделение премиальных серий на \"Потребительские\" - ноутбуки для частного использования и \"Коммерческие\" - для делового. Однако, сегодня, в отношении премиальных продуктов это разделении носит все более условный характер, и касайется в большей мере особенностей организации системы продаж. Покупателя этот момент должен волновать в меньшей степени.<br>Тем не менее привидем \"официальное\" разделение.<br> \"Потребительские серии Premium:\" <ul><li>Acer Swift 5/7</li><li>Asus Zenbook</li></ul></p>",
#     "classes": [
#         "GO_premium"
#     ]
# },

class Mth_cat(object):

    def __init__(self, Mth_, Cat_, num=0):
        self.mth_ = Mth_

        if Cat_ in ['Nb', 'Mnt', 'Ups', 'Mfp']:

            self.cat = Cat_.lower()

        # DB Tables names
            self.db_products = self.cat + '_products'
            self.db_vardata = self.cat + '_vardata'
            self.db_classes = self.cat + '_classes'
            self.db_mtm_pr_cl = self.cat + '_products' + '_has_' + 'self.cat' + '_classes'

        # JSON
            with open('rate_autogen.json', encoding='utf-8') as f_cat:
                self.json_cat = json.load(f_cat)[Cat_]

        else:
            print("Не тот Cat_: ", Cat_)
            raise

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


        # File name
        self.filename = "Autogen/" + Cat_ + "_Autogen_" + Mth_ + "_" + str(num) + ".html"
        self.file_output = open(self.filename, "w")
        print("Output -> ", self.filename)

    def Select_Classes(self, list_classes):

        if list_classes:
            tbl_classes = sql.Table(self.db_classes, self.metadata, autoload=True)
            df_classes_ = pd.read_sql(tbl_classes.select().where(tbl_classes.c.name.in_(list_classes)), self.connection)

        return df_classes_

    #def Select_Vardata_
    def Select_Top10_in_Classes(self, list_classes):



    def Autogen(self):

        for i in self.json_cat:
            print(i)
            df_classes = self.Select_Classes(self.json_cat[i]["classes"])
            print(df_classes)


###### MAIN

Jul = Mth_cat('Jul', 'Nb')
Jul.Autogen()



