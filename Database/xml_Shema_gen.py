import pandas as pd
import sqlalchemy as sql
#import json
import time
import datetime as dt
from datetime import timedelta

class DB():
    def __init__(self, list_cat):

        self.dict_cat_conn = {}
        self.list_cat = list_cat

        sql_engine = sql.create_engine("mysql://shulya403:1qazxsw2@localhost/all_gid_2?charset=utf8mb4",
                                       echo=True,
                                       encoding='utf8',
                                       convert_unicode=True)
        metadata = sql.MetaData(sql_engine)


        for i in list_cat:
            tbl_products = sql.Table(i.lower() + '_products', metadata, autoload=True)
            tbl_rate = sql.Table('txt_ratings', metadata, autoload=True)
            self.connection = sql_engine.connect()
            self.dict_cat_conn[i] = self.Select_SQL_to_df(tbl_products)

        self.df_rate = self.Select_SQL_to_df(tbl_rate)


# df из из таблицы SQL
    def Select_SQL_to_df(self, tbl):

        exit_ = pd.DataFrame()
        select_qry = tbl.select()
        exit_ = pd.read_sql(select_qry, self.connection)
        print(exit_.columns)

        return exit_

# файл

    def xml_write(self, filename):

        loc_ = list()
        lastmod_ = list()

        now = dt.datetime.now()
        now_ = time.strftime("%Y-%m-%d", time.struct_time(
                (now.year, now.month, now.day, 0, 0, 0, now.weekday(), now.day, -1)))
        for cat in self.dict_cat_conn:
            count=0
            for i, row in self.dict_cat_conn[cat].iterrows():
                loc_.append('https://allgid.ru/' + cat + '/' + str(row['id']))
                date_ = row['appear_month']
                try:
                    date_ += timedelta(days=45)
                except TypeError:
                    pass
                lastmod_.append(date_)

                count+=1
            print(cat, count)
        df = pd.DataFrame({'loc': loc_, 'lastmod': lastmod_})
        print("Всего модлей:", len(df))

        xml_f = open(filename, "w")

        xml_f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")



        xml_f.write("<url>\n<loc>https://allgid.ru/</loc>\n</url>\n")

        for cat in self.dict_cat_conn:
            tup_dt = (cat, now_)
            xml_f.write("<url>\n<loc>https://allgid.ru/{0}/</loc>\n<lastmod>{1}</lastmod>\n<changefreq>weekly</changefreq>\n<priority>0.9</priority>\n</url>\n".format(*tup_dt))

        xml_f.write("<url>\n<loc>https://allgid.ru/rate/</loc>\n<lastmod>{0}</lastmod>\n<changefreq>weekly</changefreq>\n</url>\n".format(now_))

        for cat in list(self.df_rate['cat'].unique()):
                tup_txt = (cat, now_)
                xml_f.write("<url>\n<loc>https://allgid.ru/rate/{0}/</loc>\n<lastmod>{1}</lastmod>\n<changefreq>weekly</changefreq>\n</url>\n".format(*tup_txt))
                for i, row in self.df_rate[self.df_rate['cat'] == cat][['idtxt_ratings', 'date']].iterrows():
                    tup_article = (cat, row.idtxt_ratings, row.date)
                    xml_f.write("<url>\n<loc>https://allgid.ru/rate/{0}/{1}</loc>\n<lastmod>{2}</lastmod>\n</url>\n".format(*tup_article))

        xml_f.write("<url>\n<loc>https://allgid.ru/search_all.html</loc>\n<lastmod>{0}</lastmod>\n<changefreq>weekly</changefreq>\n<priority>1.0</priority>\n</url>\n".format(
                tup_dt[1]))
        xml_f.write("<url>\n<loc>https://allgid.ru/al_about.html</loc>\n</url>\n")


        for i, row in df.iterrows():
            xml_f.write("<url>\n")
            xml_f.write("<loc>{}</loc>\n".format(row['loc']))
            if row['lastmod']:
                xml_f.write("<lastmod>{}</lastmod>\n".format(row['lastmod']))
            xml_f.write("</url>\n")
        xml_f.write("</urlset>")
        xml_f.close()

        #url_.append(self.dict_cat_conn[cat][id])


db = DB(['Nb', 'Mnt', 'Mfp', 'Ups']).xml_write('sitemap.xml')
