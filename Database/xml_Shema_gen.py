import pandas as pd
import sqlalchemy as sql
#import json
import time
import datetime as dt

class DB():
    def __init__(self, list_cat):

        self.dict_cat_conn = {}

        sql_engine = sql.create_engine("mysql://shulya403:1qazxsw2@localhost/all_gid_2?charset=utf8mb4",
                                       echo=True,
                                       encoding='utf8',
                                       convert_unicode=True)
        metadata = sql.MetaData(sql_engine)


        for i in list_cat:
            tbl_products = sql.Table(i.lower() + '_products', metadata, autoload=True)
            self.connection = sql_engine.connect()
            self.dict_cat_conn[i] = self.Select_SQL_to_df(tbl_products)


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
        for cat in self.dict_cat_conn:
            for i, row in self.dict_cat_conn[cat].iterrows():
                loc_.append('https://www.allgid.ru/' + cat + '/' + str(row['id']))
                lastmod_.append(row['appear_month'])
        df = pd.DataFrame({'loc': loc_, 'lastmod': lastmod_})
        print("Всего модлей:", len(df))

        xml_f = open(filename, "w")

        xml_f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n")

        now = dt.datetime.now()



        xml_f.write("<url>\n<loc>https://www.allgid.ru/</loc>\n</url>\n")

        for cat in self.dict_cat_conn:
            tup_dt = (cat, time.strftime("%Y-%m-%d", time.struct_time(
                (now.year, now.month, now.day, 0, 0, 0, now.weekday(), now.day, -1))))
            xml_f.write("<url>\n<loc>https://www.allgid.ru/{0}/</loc>\n<lastmod>{1}</lastmod>\n<changefreq>weekly</changefreq>\n<priority>0.9</priority>\n</url>\n".format(*tup_dt))

        xml_f.write("<url>\n<loc>https://www.allgid.ru/search_all.html</loc>\n<lastmod>{0}</lastmod>\n<changefreq>weekly</changefreq>\n<priority>1.0</priority>\n</url>\n".format(
                tup_dt[1]))
        xml_f.write("<url>\n<loc>https://www.allgid.ru/al_about.html</loc>\n</url>\n")


        for i, row in df.iterrows():
            xml_f.write("<url>\n")
            xml_f.write("<loc>{}</loc>\n<changefreq>monthly</changefreq>\n".format(row['loc']))
            if row['lastmod']:
                xml_f.write("<lastmod>{}</lastmod>\n".format(row['lastmod']))
            xml_f.write("</url>\n")
        xml_f.write("</urlset>")
        xml_f.close()

        #url_.append(self.dict_cat_conn[cat][id])


db = DB(['Nb', 'Mnt', 'Mfp']).xml_write('sitemap.xml')
