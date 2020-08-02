import pandas as pd
import sqlalchemy as sql
import json

# Изменяемые записи для Update
def df_compare(df_old, df_new):

    if set(df_old.columns) == set(df_new.columns):
        exit_ = pd.DataFrame(columns=df_old.columns)
        exit_loc = 0
        cols = set(df_old.columns) - {'name'}

        for i, row in df_new.iterrows():
            for j in cols:
                name = row['name']
                if df_old[df_old['name'] == name][j].values[0] != row[j]:
                    exit_.loc[exit_loc] = row
                    exit_loc += 1
    else:
        print("Error df_compare(df_old, df_new): Поля несовпадают")
        raise

    return exit_


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

        xl_df_Products = Get_xl(xl_page, dir_root + Category + "/" + xl_Products)

        self.df_Products = df_Products(xl_df_Products, self.dict_xl_db_Fields)
        self.df_Classes = df_Classes(xl_df_Products, self.dict_xl_db_Classes)
        self.df_Products.fillna("")
        self.df_Classes.fillna("", inplace=True)

# Databse connect
    def DB_alchemy(self,
                   category,
                   db="mysql://shulya403:1qazxsw2@localhost/all_gid_2?charset=utf8mb4"):
        self.sql_engine = sql.create_engine(db, echo=True, encoding='utf8', convert_unicode=True)

        metadata = sql.MetaData(self.sql_engine)

        sql_tbl_name_products = category+'_products'
        sql_tbl_name_class = category + '_classes'

        self.tbl_products = sql.Table(sql_tbl_name_products, metadata, autoload=True)
        self.tbl_classes = sql.Table(sql_tbl_name_class, metadata, autoload=True)

        self.connection = self.sql_engine.connect()


# Заливка df в tbl SQL
    def Insert_df_to_SQL(self, df, tbl):

            dict_insert = df.to_dict(orient='records')

            insert_qry = tbl.insert()
            self.connection.execute(insert_qry, dict_insert)

    def Update_df_in_SQL(self,df, tbl):

        cols = set(df.columns) - {'name'}
        cols = list(cols)
        for name in df['name']:
            dict_upadate = df[df['name'] == name][cols].to_dict(orient='records')
            update_qry = tbl.update().where(tbl.c.name == name).values()
            self.connection.execute(update_qry, dict_upadate)


# df из из таблицы SQL
    def Select_SQL_to_df(self, tbl):

        exit_ = pd.DataFrame()
        select_qry = tbl.select()
        exit_ = pd.read_sql(select_qry, self.connection)

        return exit_

# df имеющиеся продукты
#    def Select_SQL_Products(self):
#         df_ = self.Select_SQL_to_df(self.tbl_products)
#
#         return df_
#
#         # df имеющиеся классы
#     def Select_SQL_Classes(self):
#         df_ = self.Select_SQL_to_df(self.tbl_classes)
#
#         return df_


# сопоставление двух df. новые по полю name
    def New_names(self, df_old, df_new):

        #Новые записи
        df_old_names = set(df_old['name'])
        df_new_names = set(df_new['name'])

        difference = df_new_names - df_old_names
        coincidence = df_old_names - difference

        exit_insert = df_new[df_new['name'].isin(difference)]

        #Проверка исправленнных

        df_old_names_restrict = df_old[df_new.columns]

        #exit_update = df_new.compare(df_old_names_restrict)
        exit_update = df_compare(df_old_names_restrict, df_new[df_new['name'].isin(coincidence)])

        return (exit_insert, exit_update)

# Products_handle
    def Pruducts_to_SQL(self, df_new):

        tup_df = self.New_names(self.Select_SQL_to_df(self.tbl_products), df_new)
        df_select = tup_df[0]
        df_update = tup_df[1]

        if not df_select.empty:
            self.Insert_df_to_SQL(df_select, self.tbl_products)

        if not df_update.empty:
            self.Update_df_in_SQL(df_update, self.tbl_products)

# Classes_handle
    def Classes_to_SQL(self, df_new):
        tup_df = self.New_names(self.Select_SQL_to_df(self.tbl_classes), df_new)
        df_select = tup_df[0]
        df_update = tup_df[1]

        if not df_select.empty:
            self.Insert_df_to_SQL(df_select, self.tbl_classes)

        if not df_update.empty:
            self.Update_df_in_SQL(df_update, self.tbl_classes)

# Products_has_classes M-n-T
    def df_MtM_upgrade(self):

        df1 = pd.DataFrame({'name': ['a','b','c'],
                            'CL1':[None,1,None],
                            'CL2':[1,1,1],
                            'CL3':[None,None, 1]})
        df2 = pd.DataFrame({'name': ['b','a','c'],
                            'CL1':[1,1,None],
                            'CL2':[1,None,1],
                            'CL3':[None,None, None]})

        df3 = df1.compare(df2)
        print(df3)
        print(df3['CL1']['other'])


# MAIN

# def __init__ (self,
#                     xl_Products,
#                     xl_Vardata,
#                     dir_root = "C:\\Users\\shulya403\\Shulya403_works\\all_gid_2\\Data\\",
#                     Category='Nb',
#                     JSON_file="categories_fields.json"):

FillDB = DB_insert_from_excel(xl_Products="nb_models_06_new.xlsx",
                     xl_Vardata="NB_Report-5`20.xlsx")
#FillDB.DB_alchemy(FillDB.Category)
#FillDB.Pruducts_to_SQL(df_new=FillDB.df_Products.head(25))
#FillDB.Classes_to_SQL(df_new=FillDB.df_Classes)
FillDB.df_MtM_upgrade()

