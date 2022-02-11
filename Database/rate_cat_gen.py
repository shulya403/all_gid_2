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
        self.cat_rus = {
            'Nb': ("Ноутбуки", "ноутбуков", "Noutbuk"),
            'Mnt': ("Мониторы", "мониторов", "Monitor"),
            'Mfp': ("Устройства печати", "печатающих устройств", "Printer-mfu"),
            'Ups': ("Источники бесперебойного питания", "ИБП", "Ups")
        }


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

    def Select_Classes(self, list_classes, list_noclasses):

        tbl_classes = sql.Table(self.db_classes, self.metadata, autoload=True)

        if list_classes:
            self.df_classes_ = pd.read_sql(tbl_classes.select().where(tbl_classes.c.name.in_(list_classes)), self.connection)
        else:
            self.df_classes_ = None

        if list_noclasses:
            self.df_noclasses_ = pd.read_sql(tbl_classes.select().where(tbl_classes.c.name.in_(list_noclasses)),
                                           self.connection)
        else:
            self.df_noclasses_ = None

    def Select_Vardata(self, Mth):
        tbl_vardata = sql.Table(self.db_vardata, self.metadata, autoload=True)
        df_varadta_ = pd.read_sql(tbl_vardata.select().where(tbl_vardata.c.month == Mth), self.connection)

        return df_varadta_

    def Unselect_noclasses(self, tbl_mtm, fk_mth_products, noclasses, list_exec_products):

        print(noclasses)
        print('до отсева: {0}'.format(len(list_exec_products)))

        df_noclasses = pd.read_sql(tbl_mtm.select().
                             where(and_(tbl_mtm.c.fk_products.in_(fk_mth_products), tbl_mtm.c.fk_classes.in_(noclasses))), self.connection)
        list_exit_ = list(set(list_exec_products) - set(df_noclasses['fk_products'].unique()))

        print('после отсева: {0}'.format(len(list_exit_)))


        return list_exit_

    def Select_Top_in_Classes(self, list_classes,  list_noclasses, filds_filter):

        self.Select_Classes(list_classes, list_noclasses)
        df_vardata = self.Select_Vardata(self.mth_)
        fk_mth_products = df_vardata['fk_products'].to_list()

        try:
            fk_classes = self.df_classes_['id'].to_list()
            len_classes = len(fk_classes)
        except Exception:
            fk_classes = []
            len_classes = 0
        try:
            fk_noclasses = self.df_noclasses_['id'].to_list()
        except Exception:
            fk_noclasses = []

        tbl_mtm = sql.Table(self.db_mtm_pr_cl, self.metadata, autoload=True)
        #classes
        if fk_classes:
            #set_yno_classes = set(fk_classes) | set(fk_noclasses)
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

        #noclasses
        if list_exec_products and fk_noclasses:
            list_exec_products = self.Unselect_noclasses(tbl_mtm, fk_mth_products, fk_noclasses, list_exec_products)

        print('Длина в итоге: {}'.format(len(list_exec_products)))
        tbl_products = sql.Table(self.db_products, self.metadata, autoload=True)
        df_exec_product = pd.read_sql(tbl_products.select().where(tbl_products.c.id.in_(list_exec_products)), self.connection)

        df_exit = df_vardata.merge(df_exec_product, left_on='fk_products', right_on='id', how='inner')
        print(df_exit.columns)
        # Фильтры по ТТХ
        set_df_fld = set(df_exit.columns) - {'id_x', 'month', 'fk_products', 'id_y'}
        # and', 'name', 'type', 'prt_technology', 'color', 'format_a', 'fax',
        #        'duplex', 'photo', 'usb', 'wi_fi', 'ethernet', 'appear_month', 'speed'],
        #
        if filds_filter:
            for fld in filds_filter:
                if fld in set_df_fld:
                    dict_fld = filds_filter[fld]

                    if ("=" in dict_fld) and dict_fld['=']:
                        df_exit = df_exit[df_exit[fld] == dict_fld['=']]
                    if ("!=" in dict_fld) and dict_fld['!=']:
                        df_exit = df_exit[df_exit[fld] != dict_fld['!=']]
                    if ("like" in dict_fld) and dict_fld['like']:
                        df_exit = df_exit[df_exit[fld].str.contains(str(dict_fld['like']), regex=False)]
                    if (">" in dict_fld) and dict_fld['>'] and (df_exit[fld].dtype in ['int64', 'float64']):
                        df_exit = df_exit[df_exit[fld] > dict_fld['>']]
                    if ("<" in dict_fld) and dict_fld['<'] and (df_exit[fld].dtype in ['int64', 'float64']):
                        df_exit = df_exit[df_exit[fld] < dict_fld['<']]
                    if ("isin" in dict_fld) and dict_fld['isin']:
                        df_exit = df_exit[df_exit[fld].isin(dict_fld['isin'])]
                    if ("isnoin" in dict_fld) and dict_fld['isnoin']:
                        df_exit = df_exit[~df_exit[fld].isin(dict_fld['isnoin'])]
        print('Длина после фильтра: {}'.format(len(df_exit)))


        df_ = df_exit.sort_values(by=['sales_units'], ascending=False)

        return df_

    def Autogen(self, general_header):

        def TTX_Table_Fields(jsn_, columns_):

            if "ttx_show" in jsn_.keys():
                return list(jsn_.keys())
            else:
                return list(set(columns_) - {'id', 'brand', 'name', 'id_brand_name', 'appear_month', 'id_x', 'month', 'sales_units'})

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

        self.file_output.write("<p>{0}</p>\n".format(self.Transliterate(general_header)))
        self.file_output.write("<h1>{0}</h1>\n\n".format(general_header))

        for i in self.json_cat:

            jsn_ = self.json_cat[i]
            classes_yes = jsn_['classes']
            if "noclasses" in jsn_.keys():
                if jsn_['noclasses']:
                    classes_no = jsn_['noclasses']
                else:
                    classes_no = []
            else:
                classes_no = []
            if "filds_filter" in list(jsn_.keys()):
                filds_filter = jsn_['filds_filter']
            else:
                filds_filter = {}

            df_ = self.Select_Top_in_Classes(classes_yes, classes_no, filds_filter)
            try:
                lead_model_name = df_.iloc[0]['name']
            except IndexError:
                continue
            ser_min_price_name = df_.loc[df_[['price_rur']].idxmin()].iloc[0][['brand', 'name', 'id_brand_name', 'price_rur','id_y']]
            df_price_q = df_[0:top_q_handler(len(df_), Q_tbl(jsn_))].sort_values(by=['price_rur'])

            self.Write_to_file_article_body(lead_model_name, ser_min_price_name, df_price_q, jsn_)

        self.file_output.write("\n<!-- ################ -->\n<!-- ### Keywords ### -->\n\n")

        # Keywords
        self.file_output.write("<div class=\"inarticle-rignt-filter\">\n")
        self.file_output.write(
            "<h3><a href = \"/{0}/?tabs=marketability\">Выбрать {1} для своих целей</a></h3>".format(
                self.cat_rus[self.cat.title()][2], self.cat_rus[self.cat.title()][0].lower()))
        self.file_output.write(
            "<div class=\"filter_button_big\">\n<div class =\"fltr_pic\"><a href=\"/{0}/?tabs=marketability\">&nbsp;</a></div>".format(
                self.cat_rus[self.cat.title()][2]))
        self.file_output.write(
            "<div class=\"fltr_text\"><a href=\"/{0}/?tabs=marketability\">ФИЛЬТР</a></div>\n</div>\n</div>\n\n".format(
                self.cat_rus[self.cat.title()][2]))

        for i in self.json_cat:

            jsn_ = self.json_cat[i]
            classes_yes = jsn_['classes']
            if "noclasses" in jsn_.keys():
                if jsn_['noclasses']:
                    classes_no = jsn_['noclasses']
            else:
                classes_no = []
            if "filds_filter" in list(jsn_.keys()):
                filds_filter = jsn_['filds_filter']
            else:
                filds_filter = {}

            df_ = self.Select_Top_in_Classes(classes_yes, classes_no, filds_filter)

            self.Write_to_file_keywors(jsn_, self.List_Classses_Text(self.df_classes_), self.List_Classes_HTML(self.df_classes_))


        self.file_output.write("</body></html>")

    def List_Classses_Text(self, df_classes):

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
                            string_out += "<br />&#171;" + row['class_subtype'] +": "
                            used_subtype.add(row['class_subtype'])
                       else:
                           string_out += "; &#187;"
                    else:
                        string_out += "&#171;"
                    string_out += row['text'] + "&#187;;"

                return string_out
            except Exception as Err:
                print("Err")
                return ""

    def List_Classes_HTML(self, df_classes):

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

    def Transliterate(self, str_):
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
            "я": "ya",
            "`": "-",
            ".": "-",
            ",": "",
            "\"": "inch",
            ":": "-"
        }

        exit_ = ""
        for symbol in str_.lower():
            try:
                change = article_name_transliterate[symbol]
                exit_ += change
            except KeyError:
                exit_ += symbol
        return exit_

    def Write_to_file_article_body(self, lead_model_name, ser_min_price_name, df_price_q, jsn_):

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
            12: ("декабре", "Декабрь")
        }

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

        def P_Leader_Model(Lead_model_row, Mth, Cat, tbl_sign):

            year_ = str(Mth.year)
            mth_ = mth_padege[Mth.month][0]
            #cat_ = self.cat_rus[Cat.title()][1]
            leader_model = Lead_model_row.loc['brand'] + " " + Lead_model_row.loc['name']
            href_model = "/" + Cat.title() + "/" + str(Lead_model_row['id_brand_name'])
            if tbl_sign:
                string_out = "В {0} {1} г. лидером продаж в сегменте <em>&#171;{2}&#187;</em> стала модель <strong><a href=\"{3}\" target=\"_blank\">{4}</a></strong>, стоимостью примерно {5} тыс. руб.".\
                    format(mth_, year_, tbl_sign, href_model, leader_model, int(round(Lead_model_row['price_rur']/1000, 0)))
            else:
                string_out = "В {0} {1} г. лидером продаж стала модель <strong><a href=\"{2}\" target=\"_blank\">{3}</a></strong>.". \
                    format(mth_, year_, href_model, leader_model, Lead_model_row['price_rur'])
            return string_out

        cl_gl_name = jsn_['cl_gl_name']
        tbl_sign = jsn_['table_sign']
        self.file_output.write("<!-- ### {0} ###-->\n".format(tbl_sign))
        self.file_output.write("<!-- ########### -->\n\n")

        header_mth = jsn_['header'] + ". " + mth_padege[self.mth_.month][1] + "`" + str(self.mth_.year)[2:]
        #self.file_output.write("<a href=\"#{0}\">{1}</a>\n\n".format(cl_gl_name, header_mth))
        self.file_output.write("\n{0}\n".format(self.Transliterate(header_mth)))
        self.file_output.write("<h2 id=\"{0}\" name=\"{0}\">{1}</h2>\n\n".format(cl_gl_name, header_mth))

        self.file_output.write(
            "<p><em>Источник: аналитическая компания <a href=\"https://itbestsellers.ru\" target=\"_blank\">ITResearch</a>, проект <a href=\"https://allgid.ru\">allgid.ru \"Гид покупателя\"</a>\n<br>\nДанные по рынку России</em>\n</p>\n")

        # self.file_output.write("<p><em>Источник: аналитическая компания <a href=\"https://itbestsellers.ru\" target=\"_blank\">ITResearch</a>, проект <a href=\"https://allgid.ru\">allgid.ru \"Гид покупателя\"</a>\n<br>\nДанные по рынку России</em>\n</p>\n")
        self.file_output.write("<div class=\"inarticle_cit1\">{0}</div>\n\n".format(jsn_['cat_description']))

        classes_ = self.List_Classses_Text(self.df_classes_)
        classes_html = self.List_Classes_HTML(self.df_classes_)
        lead_model_row_ = df_price_q[df_price_q['name'] == lead_model_name].iloc[0]
        self.file_output.write("<p>{0}".format(P_Leader_Model(lead_model_row_, self.mth_, self.cat_rus[self.cat.title()][2], tbl_sign)))
        if lead_model_row_.loc['name'] != ser_min_price_name['name']:
            self.file_output.write("</p>\n<p>Самым же недорогим устройством данного класса является модель <a href=\"{0}\" target=\"_blank\">{1}</a> стоимостью {2} тыс. руб. в среднем.</p>\n\n".
                                   format("/" + self.cat_rus[self.cat.title()][2] + "/" + str(ser_min_price_name['id_brand_name']),
                                    ser_min_price_name['brand'] + " " + ser_min_price_name['name'],
                                    round(ser_min_price_name['price_rur'] / 1000, 1)))
        else:
            self.file_output.write(" И это - самое доступное по цене устройство в данном классе. </p>\n")

        self.file_output.write(
            "<h3>{1}: Top-{2}, в {3}</h3>\n<em>(Сортировка - по возрастанию средней цены)</em>\n".format(self.cat_rus[self.cat.title()][0],
                                                                jsn_['table_sign'],
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
            self.file_output.write("<th><a href=\"/{0}/{1}\">{2}</a></th>\n".format(self.cat_rus[self.cat.title()][2], row['id_brand_name'], crown + row['brand'] + " " + row['name']))
            self.file_output.write("<td>{0}</td>\n".format(digit_separator(row['price_rur'])))
            try:
                for ttx in jsn_["ttx_show"]:
                    self.file_output.write("<td>{0}</td>\n".format(row[ttx]))
            except KeyError:
                pass
            self.file_output.write("</tr>\n")
        self.file_output.write("</tbody></table></div></div>")


        try:
            self.file_output.write("<p><strong><a href=\"/{0}/{1}\">Полный рейтинг Топ-20 популярных {2} типа <em>{3}</em> &#8921;</a></strong></p>\n".format(self.cat.title(), classes_html, self.cat_rus[self.cat.title()][1], classes_))
        except Exception:
            self.file_output.write("<p><strong><a href=\"/{0}/{1}\">Полный рейтинг Топ-20 популярных {2} &#8921;</a></strong></p>\n".format(self.cat.title(), classes_html, self.cat_rus[self.cat.title()][1]))


    def Write_to_file_keywors(self, jsn_, classes_, classes_html):


        try:
            self.file_output.write("<div>\n<div class=\"inarticle-rignt-filter\">\n")
            self.file_output.write("<h3><a href=\"/{0}/{1}\">Top-20 {2}</a></h3>\n".format(self.cat.title(), classes_html, jsn_['table_sign']))

            for i, row in self.df_classes_.iterrows():
                self.file_output.write("<div class=\"filters-item-check\">\n")
                self.file_output.write("<div class=\"filters-item-check-galka\">\n")
                self.file_output.write("<a href=\"/{0}/{1}\">&nbsp;</a></div>\n".format(self.cat.title(), classes_html))
                self.file_output.write("<a href=\"/{0}/{1}\">{2} </a>\n</div>\n".format(self.cat.title(), classes_html, row['text']))
            self.file_output.write("</div></div>\n\n")
        except Exception:
            pass

###### MAIN

# Jul = Mth_cat('Aug', 2021, 'Mnt', top_q=5, num="game")
# Jul.Autogen()

# Obj = Mth_cat('Sep', 2021, 'Mnt', top_q=5, num="Mnt_9_office_reprice", )
# Obj.Autogen(general_header="Рейтинг популярности мониторов для офиса. Сентябрь 2021")

Obj = Mth_cat(Mth_='Dec', Year_=2021, Cat_='Mnt', top_q=5, num="Mnt Dec Gamer v2")
Obj.Autogen(general_header="Игровые мониторы-бестселлеры. Декабрь-21")

