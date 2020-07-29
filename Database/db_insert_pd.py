import pandas as pd
import sqlalchemy as sql
import json

class DB_insert_from_excel(object):
    def __init__ (self,
                    xl_Products,
                    xl_Vardata,
                    dir_root = "../Data/",
                    Category='Nb',
                    JSON_file="categories_fields.json"):

        self.Category = Category

# Формирование словаря из JSON для Products - ТТХ "Fields_products"
        def Get_dict_xl_TTX(dict_):
            exit = dict()
            if dict_:
                if dict_["Fields_products"]:
                    for i in dict_["Fields_products"]:
                        exit[i] = dict_["Fields_products"][i]['db_name']
            return exit

# Формирование словаря из JSON для Classes & Goals "Filds_classes"
        def Get_dict_xl_CL_GO(dict_):
            exit = dict()
            if dict_:
                if dict_["Fields_classes"]:
                   exit = dict_["Fields_classes"]
            return exit

# Данные из таблицы моделей для Products, c ТТХ, классами и целями
        def Get_xl(page, filename):

            if page:
                try:
                    df_ = pd.read_excel(filename, sheet_name=page)
                except Exception:
                    df_ = pd.read_excel(filename)
            else:
                df_ = pd.read_excel(filename)

            print("Таблца из Excel для {} \n {}".format(self. Category, df_.columns))

            return df_

# Модели и ТТХ с пределкой намиенование полей согласно JSON "Fields_products"
        def df_Products(df_file, dict_fields):

            df_ = df_file.copy()

            list_xl_Fields = list(dict_fields.keys())

            for col in df_:
                if col not in list_xl_Fields:
                    df_.drop(col, axis='columns', inplace=True)

            df_.rename(mapper=dict_fields, axis='columns', inplace=True)

            print("df_Pruducts \n", df_.head())

            return df_

# Классы и цели согласно JSON "Filds_classes"
        def df_Classes(df_file, dict_fields):

            if dict_fields:
                xl_Classes_n_Goals = list(dict_fields.keys())
            else:
                xl_Classes_n_Goals = list()
            df_ = pd.DataFrame(columns=['name', 'text', 'explanation', 'class_subtype', 'type'])


            if xl_Classes_n_Goals:
                i = 0
                for col in df_file.columns:
                    if col in xl_Classes_n_Goals:
                        df_.loc[i, 'name'] = col
                        for fld in dict_fields[col]:
                            df_.loc[i, fld] = dict_fields[col][fld]
                        i += 1
            print(df_)
            if df_['type'].isna().any():
                print("Отсутсвует обозначение типа для полей")
                print(df_[df_['type'].isna()]['name'])
                raise
            uncorrect_class_type = set(df_['type'].values) - {'CL', 'GO'}
            if uncorrect_class_type:
                print("Неправильный тип поля {} в {}".format(uncorrect_class_type,
                                                             df_[df_['type'].isin(list(uncorrect_class_type))]['name']))
                raise


            return df_

        with open(JSON_file, encoding='utf-8') as f:
            dict_xl_Fields = json.load(f)

        if dict_xl_Fields:
            try:
                dict_xl_Cat_Fields = dict_xl_Fields[self.Category]
            except Exception:
                dict_xl_Cat_Fields = dict()
                print("Нет такой категории в фале JSON_File")
        else:
            print("Непонятки с файлом JSON_file")
            dict_xl_Cat_Fields = dict()

        self.dict_xl_db_Fields = Get_dict_xl_TTX(dict_xl_Cat_Fields)
        self.dict_xl_db_Classes = Get_dict_xl_CL_GO(dict_xl_Cat_Fields)

        try:
            xl_page = dict_xl_Cat_Fields["xl_page"]
        except KeyError:
            xl_page = ""

        #xl_df_Products = Get_xl(xl_page, dir_root + Category + "/" + xl_Products)

        #self.df_Products = df_Products(xl_df_Products, self.dict_xl_db_Fields)
        #self.df_Classes = df_Classes(xl_df_Products, self.dict_xl_db_Classes)

# Databse connect
        self.sql_engine = sql.create_engine("mysql://shulya403:1qazxsw2@localhost/all_gid_2", echo=True)

        print(self.sql_engine.table_names())

# Заливка Pruducts
    def Insert_SQL_Entity(self, df):
        pass


# Скачивание из Datatbase



# MAIN

# def __init__ (self,
#                     xl_Products,
#                     xl_Vardata,
#                     dir_root = "C:\\Users\\shulya403\\Shulya403_works\\all_gid_2\\Data\\",
#                     Category='Nb',
#                     JSON_file="categories_fields.json"):

DB_insert_from_excel(xl_Products="nb_models_06_new.xlsx",
                     xl_Vardata="NB_Report-5`20.xlsx")

