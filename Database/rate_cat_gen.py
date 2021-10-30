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
        self.file_output = open(self.filename, "w", encoding='utf8')
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
        else:
            self.df_classes_ = None

    def Select_Vardata(self, Mth):
        tbl_vardata = sql.Table(self.db_vardata, self.metadata, autoload=True)
        df_varadta_ = pd.read_sql(tbl_vardata.select().where(tbl_vardata.c.month == Mth), self.connection)

        return df_varadta_

    def Select_Top_in_Classes(self, list_classes):

        self.Select_Classes(list_classes)
        df_vardata = self.Select_Vardata(self.mth_)
        fk_mth_products = df_vardata['fk_products'].to_list()

        try:
            fk_classes = self.df_classes_['id'].to_list()
            len_classes = len(fk_classes)
        except Exception:
            fk_classes = []
            len_classes = 0



        tbl_mtm = sql.Table(self.db_mtm_pr_cl, self.metadata, autoload=True)
        if fk_classes:
            df_mtm = pd.read_sql(tbl_mtm.select().
                             where(and_(tbl_mtm.c.fk_products.in_(fk_mth_products), tbl_mtm.c.fk_classes.in_(fk_classes))), self.connection)
        else:
            df_mtm = pd.read_sql(tbl_mtm.select().
                                 where(tbl_mtm.c.fk_products.in_(fk_mth_products)), self.connection)
        df_agg_mtm = df_mtm[['fk_products', 'fk_classes']].groupby('fk_products').count()

        if fk_classes:
            list_exec_products = df_agg_mtm[df_agg_mtm['fk_classes'] == len_classes].index.to_list()
        else:
            list_exec_products = df_agg_mtm.index.to_list()
        tbl_products = sql.Table(self.db_products, self.metadata, autoload=True)
        df_exec_product = pd.read_sql(tbl_products.select().where(tbl_products.c.id.in_(list_exec_products)), self.connection)

        df_exit = df_vardata.merge(df_exec_product, left_on='fk_products', right_on='id', how='inner')
        df_ = df_exit.sort_values(by=['sales_units'], ascending=False)

        return df_

    def Autogen(self):

        def TTX_Table_Fields(jsn_, columns_):

            if "ttx_show" in jsn_.keys():
                return list(jsn_.keys())
            else:
                return list(set(columns_) - {'id', 'brand', 'name', 'appear_month', 'id_x', 'month', 'sales_units'})

        def Q_tbl(jsn_):
            if "q_table" in jsn_.keys():
                return jsn_['q_table']
            else:
                return 10

        def top_q_handler(len_df, top_q):
            if len_df < top_q:
                return len_df
            else:
                return top_q

        self.file_output.write("<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n<title>{0}</title>\n</head>\n<body>\n".format(self.cat.title() + self.mth_.strftime("  %b `%Y")))

        for i in self.json_cat:

            jsn_ = self.json_cat[i]
            print(i)
            df_ = self.Select_Top_in_Classes(jsn_['classes'])
            lead_model_name = df_.iloc[0]['name']
            ser_min_price_name = df_.loc[df_[['price_rur']].idxmin()].iloc[0][['brand', 'name', 'price_rur','id_y']]
            df_price_q = df_[0:top_q_handler(len(df_), Q_tbl(jsn_))].sort_values(by=['price_rur'])

            self.Write_to_file(lead_model_name, ser_min_price_name, df_price_q, jsn_)

        self.file_output.write("</body></html>")


    def Write_to_file(self, lead_model_name, ser_min_price_name, df_price_q, jsn_):

        mth_padege = {
            1: ("январе", "Январь"),
            2: ("феврале", "Февраль"),
            3: ("марте", "Март"),
            4: ("апреле", "Апрель"),
            5: ("мае", "Май"),
            6: ("июне", "Июнь"),
            7: ("июле", "Июль"),
            8: ("августе", "Август"),
            9: ("сентябре", "Сентябрь"),
            10: ("октябре", "Октябрь"),
            11: ("ноябре", "Ноябрь"),
            12: ("декабре", "Декабре")
        }

        cat_rus = {
            'Nb': ("Ноутбуки", "ноутбуков"),
            'Mnt': ("Мониторы", "мониторов"),
            'Mfp': ("Устройства печати", "печатающих устройств"),
            'Ups': ("Источники бесперебойного питания", "ИБП")
        }

        def Transliterate(str_):
            article_name_transliterate = {
                " ": "-",
                "а": "a",
                "б": "b",
                "в": "v",
                "г": "g",
                "д": "d",
                "е": "e",
                "ё": "yo",
                "ж": "zh",
                "з": "z",
                "и": "i",
                'й': "j",
                "к": "k",
                "л": "l",
                "м": "m",
                "н": "n",
                "о": "o",
                "п": "p",
                "р": "r",
                "с": "s",
                "т": "t",
                "у": "u",
                "ф": "f",
                "х": "kh",
                "ц": "ts",
                "ч": "ch",
                "ш": "sh",
                "щ": "shch",
                "ь": "",
                "ы": "y",
                "ъ": "",
                "э": "e",
                "ю": "iu",
                "я": "ia",
                "`": "",
                ".": "__",
                ",": "_",
                "\"": "inch",
                ":": "--"
            }

            exit_ = ""
            for symbol in str_.lower():
                try:
                    change = article_name_transliterate[symbol]
                    exit_ += change
                except KeyError:
                    exit_ += symbol
            return exit_

        def List_Classses_Text(df_classes):

            try:
                #exit_ = list()
                used_subtype = set()
                df_classes_sort_cl = df_classes[df_classes['type'] == 'CL'].sort_values(by=['class_subtype'])
                df_classes_sort_go = df_classes[df_classes['type'] == 'GO'].sort_values(by=['class_subtype'])
                df_classes_sort = pd.concat([df_classes_sort_go, df_classes_sort_cl])

                string_out = ""
                for i, row in df_classes_sort.iterrows():
                    if row['class_subtype']:
                       if row['class_subtype'] not in used_subtype:
                            string_out += "&#171;" + row['class_subtype'] +": "
                            used_subtype.add(row['class_subtype'])
                       else:
                           string_out += "; &#187;"
                    else:
                        string_out += "&#171;"
                    string_out += row['text'] + "&#187;; "

                return string_out
            except Exception as Err:
                print("Err")
                return ""

        def List_Classes_HTML(df_classes):

            try:

                string_out = "?"
                for i, row in df_classes.iterrows():
                    if " " in row['name']:
                        cl_name = row['name'].replace(" ", "+")
                    else:
                        cl_name = row['name']
                    string_out += cl_name + "=Yes&"

                string_out += "tabs=marketability"

                return string_out
            except Exception:
                return "?tabs=marketability"

        def digit_separator(digit):
            if digit:
                try:
                    str_digit = str(int(digit))
                except Exception:
                    return 'n/a'
                exit_ = str()
                tail = len(str_digit) % 3
                for i in range(len(str_digit) - 3, -1, -3):
                    exit_ = "\xa0" + str_digit[i:i + 3] + exit_

                if tail != 0:
                    exit_ = str_digit[:tail] + exit_
                    return exit_
                else:
                    return exit_[1:]
            else:
                return 'n/a'


        def P_Leader_Model(Lead_model_row, Mth, Cat, Classes_):

            year_ = str(Mth.year)
            mth_ = mth_padege[Mth.month][0]
            cat_ = cat_rus[Cat.title()][1]
            leader_model = Lead_model_row.loc['brand'] + " " + Lead_model_row.loc['name']
            href_model = "/" + Cat.title() + "/" + str(Lead_model_row['id_y'])
            if Classes_:
                #str_classes = Classes_#[0]
                # if len(Classes_) > 1:
                #     for i in Classes_[1:len(Classes_)]:
                #         str_classes += "; " + i
                string_out = "В {0} {1} г. лидером продаж в сегменте {2} <em>{3}</em> стала модель <strong><a href=\"{4}\" target=\"_blank\">{5}</a></strong>.".\
                    format(mth_, year_, cat_, Classes_, href_model, leader_model)
            else:
                string_out = "В {0} {1} г. лидером продаж стала модель <strong><a href=\"{2}\" target=\"_blank\">{3}</a></strong>.". \
                    format(mth_, year_, href_model, leader_model)
            return string_out

        cl_gl_name = jsn_['cl_gl_name']
        self.file_output.write("<!-- ### {0} ###-->\n".format(cl_gl_name))
        self.file_output.write("<!-- ########### -->\n\n")

        header_mth = jsn_['header'] # + ". " + mth_padege[self.mth_.month][1] + "` " + str(self.mth_.year)[2:]
        self.file_output.write("<p>{0}</p>\n".format(Transliterate(header_mth)))
        self.file_output.write("<h2 id=\"{0}\" name=\"{0}\">{1}</h2>\n\n".format(cl_gl_name, header_mth))

        self.file_output.write("<p><em>Источник: аналитическая компания <a href=\"https://itbestsellers.ru\" target=\"_blank\">ITResearch</a>, проект <a href=\"https://allgid.ru\">allgid.ru \"Гид покупателя\"</a>\n<br>\nДанные по рынку России</em>\n</p>\n")
        self.file_output.write("<div class=\"inarticle_cit1\">{0}</div>\n\n".format(jsn_['cat_description']))

        classes_ = List_Classses_Text(self.df_classes_)
        lead_model_row_ = df_price_q[df_price_q['name'] == lead_model_name].iloc[0]
        self.file_output.write("<p>{0}".format(P_Leader_Model(lead_model_row_, self.mth_, self.cat, classes_)))
        if lead_model_row_.loc['name'] != ser_min_price_name['name']:
            self.file_output.write("</p>\n<p>Самым же недорогим устройством данного класса является модель <a href=\"{0}\" target=\"_blank\">{1}</a> стоимостью {2} тыс. руб. в среднем.</p>\n\n".
                                   format("/" + self.cat.title() + "/" + str(ser_min_price_name['id_y']),
                                    ser_min_price_name['brand'] + " " + ser_min_price_name['name'],
                                    round(ser_min_price_name['price_rur'] / 1000, 1)))
        else:
            self.file_output.write(" Она же - самое доступное по цене устройство в данном классе ноутбуков. </p>\n")

        self.file_output.write(
            "<h3>{0} класса {1}: Top-{2}, в {3}</h3> \n".format(cat_rus[self.cat.title()][0],
                                                                jsn_['cl_gl_name'],
                                                                len(df_price_q),
                                                                mth_padege[self.mth_.month][0] + " `" + str(self.mth_.year)[2:]))
        self.file_output.write("<div class=\"inarticle_table_wrap_outer\">\n<div class=\"inarticle_table_wrap\">\n<table class=\"inarticle_table\">\n<thead>\n<tr>\n")


        self.file_output.write("<th>Название</th>\n<th>Цена</th>\n")
        try:
            for ttx in jsn_["ttx_show"]:
                self.file_output.write("<th>{0}</th>\n".format(jsn_["ttx_show"][ttx]))
        except KeyError:
            pass
        self.file_output.write("</tr>\n</thead>\n<tbody>\n")

        for i, row in df_price_q.iterrows():
            if row['name'] == lead_model_row_.loc['name']:
                tr_top = " class=\"tr-top\""
                crown = "&#9812; "
            else:
                tr_top, crown = "", ""

            self.file_output.write("<tr{0}>\n".format(tr_top))
            self.file_output.write("<th><a href=\"/{0}/{1}\">{2}</a></th>\n".format(self.cat.title(), row['id_y'],crown + row['brand'] + " " + row['name']))
            self.file_output.write("<td>{0}</td>\n".format(digit_separator(row['price_rur'])))
            try:
                for ttx in jsn_["ttx_show"]:
                    self.file_output.write("<td>{0}</td>\n".format(row[ttx]))
            except KeyError:
                pass
            self.file_output.write("</tr>\n")
        self.file_output.write("</tbody></table></div></div>")

        classes_html = List_Classes_HTML(self.df_classes_)
        try:
            self.file_output.write("<p><strong><a href=\"/{0}/{1}\">Полный рейтинг Top-20 популярных {2} типа <em>{3}</em> &#8921;</a></strong></p>\n".format(self.cat.title(), classes_html, cat_rus[self.cat.title()][1], classes_))
        except Exception:
            self.file_output.write("<p><strong><a href=\"/{0}/{1}\">Полный рейтинг Top-20 популярных {2} &#8921;</a></strong></p>\n".format(self.cat.title(), classes_html, cat_rus[self.cat.title()][1]))
        self.file_output.write("\n<!-- ################ -->\n<!-- ### Keywords ### -->\n\n")
        self.file_output.write("<div class=\"inarticle-rignt-filter\">\n")
        self.file_output.write("<h3><a href = \"/{0}/?tabs=marketability\">Выбрать {1} для своих целей</a></h3>".format(self.cat.title(), cat_rus[self.cat.title()][0].lower()))
        self.file_output.write("<div class=\"filter_button_big\">\n<div class =\"fltr_pic\"><a href=\"/{0}/?tabs=marketability\">&nbsp;</a></div>".format(self.cat.title()))
        self.file_output.write("<div class=\"fltr_text\"><a href=\"/{0}/?tabs=marketability\">ФИЛЬТР</a></div>\n</div>\n</div>\n\n".format(self.cat.title()))

        try:
            self.file_output.write("<div>\n<div class=\"inarticle-rignt-filter\">\n")
            self.file_output.write("<h3><a href=\"/{0}/{1}\">Top-20 {2}</a></h3>\n".format(self.cat.title(), classes_html, jsn_['cl_gl_name']))

            for i, row in self.df_classes_.iterrows():
                self.file_output.write("<div class=\"filters-item-check\">\n")
                self.file_output.write("<div class=\"filters-item-check-galka\">\n")
                self.file_output.write("<a href=\"/{0}/{1}\">&nbsp;</a></div>\n".format(self.cat.title(), classes_html))
                self.file_output.write("<a href=\"/{0}/{1}\">{2} </a>\n</div>\n".format(self.cat.title(), classes_html, row['text']))
            self.file_output.write("</div></div>\n\n")
        except Exception:
            pass
###### MAIN

Jul = Mth_cat('Aug', 2021, 'Mnt', top_q=5, num="game")
Jul.Autogen()



