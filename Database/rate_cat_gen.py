import pandas as pd
import sqlalchemy as sql
from sqlalchemy.sql import and_
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

    def __init__(self, Mth_, Year_, Cat_, top_q=10, num=0):
        self.mth_ = self.Date_Handler(Mth_, Year_)
        print(self.mth_)
        self.top_q = top_q

        if Cat_ in ['Nb', 'Mnt', 'Ups', 'Mfp']:

            self.cat = Cat_.lower()

        # DB Tables names
            self.db_products = self.cat + '_products'
            self.db_vardata = self.cat + '_vardata'
            self.db_classes = self.cat + '_classes'
            self.db_mtm_pr_cl = self.cat + '_products' + '_has_' + self.cat + '_classes'

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

    def Date_Handler(self, Mth, Year):

        mt_names = {
            'Jan': dt.date(Year, 1, 1),
            'Feb': dt.date(Year, 2, 1),
            'Mar': dt.date(Year, 3, 1),
            'Apr': dt.date(Year, 4, 1),
            'May': dt.date(Year, 5, 1),
            'Jun': dt.date(Year, 6, 1),
            'Jul': dt.date(Year, 7, 1),
            'Aug': dt.date(Year, 8, 1),
            'Sep': dt.date(Year, 9, 1),
            'Oct': dt.date(Year, 10, 1),
            'Nov': dt.date(Year, 11, 1),
            'Dec': dt.date(Year, 12, 1),
        }

        try:
            return mt_names[Mth]
        except KeyError:
            print('Неправильный месяц: ', Mth)
            raise

    def Select_Classes(self, list_classes):

        if list_classes:
            tbl_classes = sql.Table(self.db_classes, self.metadata, autoload=True)
            self.df_classes_ = pd.read_sql(tbl_classes.select().where(tbl_classes.c.name.in_(list_classes)), self.connection)

    def Select_Vardata(self, Mth):
        tbl_vardata = sql.Table(self.db_vardata, self.metadata, autoload=True)
        df_varadta_ = pd.read_sql(tbl_vardata.select().where(tbl_vardata.c.month == Mth), self.connection)

        return df_varadta_

    def Select_Top_in_Classes(self, list_classes):

        def top_q_handler(len_df, top_q):
            if len_df < top_q:
                return len_df
            else:
                return top_q

        self.Select_Classes(list_classes)
        df_vardata = self.Select_Vardata(self.mth_)

        fk_classes = self.df_classes['id'].to_list()
        len_classes = len(fk_classes)
        fk_mth_products = df_vardata['fk_products'].to_list()


        tbl_mtm = sql.Table(self.db_mtm_pr_cl, self.metadata, autoload=True)
        df_mtm = pd.read_sql(tbl_mtm.select().
                             where(and_(tbl_mtm.c.fk_products.in_(fk_mth_products), tbl_mtm.c.fk_classes.in_(fk_classes))), self.connection)

        df_agg_mtm = df_mtm[['fk_products', 'fk_classes']].groupby('fk_products').count()

        list_exec_products = df_agg_mtm[df_agg_mtm['fk_classes'] == len_classes].index.to_list()
        tbl_products = sql.Table(self.db_products, self.metadata, autoload=True)
        df_exec_product = pd.read_sql(tbl_products.select().where(tbl_products.c.id.in_(list_exec_products)), self.connection)

        df_exit = df_vardata.merge(df_exec_product, left_on='fk_products', right_on='id', how='inner')
        df_ = df_exit.sort_values(by=['sales_units'], ascending=False)

        return df_[0:top_q_handler(len(df_), self.top_q)]

    def Autogen(self):

        for i in self.json_cat:
            print(i)
            df_ = self.Select_Top_in_Classes(self.json_cat[i]["classes"])
            print(df_)



###### MAIN

Jul = Mth_cat('Jul', 2021, 'Nb', top_q=5)
Jul.Autogen()



