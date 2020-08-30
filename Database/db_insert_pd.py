import pandas as pd
import sqlalchemy as sql
import json
import time
import datetime as dt

# Изменяемые записи для Update
def df_compare(df_old, df_new):

    if set(df_old.columns) == set(df_new.columns):
        exit_ = pd.DataFrame(columns=df_old.columns)
        exit_loc = 0
        cols = set(df_old.columns) - {'name'}

        for i, row in df_new.iterrows():
            for j in cols:
                name = row['name']
                if df_old[df_old['name'] == name][j].values[0] != str(row[j]):
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

# Формирование словаря из JSON для Полей в файле продаж
        def Get_dict_xl_Mth_Sales(dict_):
                exit = dict()
                if dict_:
                    if dict_["Fields_sales"]:
                        exit = dict_["Fields_sales"]
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
# Месячные данные по продажам для vardata
        def df_Vardata(df_file, dict_fields):

            df_ = df_file.copy()

            list_fileds = [i for i in dict_fields]

            dict_rename_fld = dict()
            for fld in list_fileds:
                col = dict_fields[fld]['col_name']
                dict_rename_fld[col] = fld
            df_.rename(mapper=dict_rename_fld, axis='columns', inplace=True)
            list_col_to_delete = list(set(df_.columns) - set(list_fileds))
            df_.drop(columns=list_col_to_delete, axis='columns', inplace=True)

            for fld in df_.columns:
                if "change" in dict_fields[fld].keys():
                    df_[fld] = df_[fld].map(dict_fields[fld]["change"])

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
        self.dict_xl_db_Vardata = Get_dict_xl_Mth_Sales(dict_xl_Cat_Fields)

        try:
            xl_products_page = dict_xl_Cat_Fields["xl_page"]
        except KeyError:
            xl_products_page = ""

        self.xl_df_Products = Get_xl(xl_products_page, dir_root + Category + "/" + xl_Products)

        try:
            xl_vardata_page = dict_xl_Cat_Fields["xl_sales_page"]
        except KeyError:
            xl_vardata_page = ""

        self.xl_df_Vardata = Get_xl(xl_vardata_page, dir_root + Category + "/" + xl_Vardata)


        self.df_Products = df_Products(self.xl_df_Products, self.dict_xl_db_Fields)
        self.df_Products.fillna("", inplace=True)
        self.df_Classes = df_Classes(self.xl_df_Products, self.dict_xl_db_Classes)
        self.df_Classes.fillna("", inplace=True)
        self.df_Vardata = df_Vardata(self.xl_df_Vardata, self.dict_xl_db_Vardata)
        self.df_Vardata.fillna("", inplace=True)

# MtM Products_Classes из SQL и Excel

    def df_MtM_Products_Classes(self):

        df_sql_Proucts = self.Select_SQL_to_df(self.tbl_products)
        df_sql_Classes = self.Select_SQL_to_df(self.tbl_classes)

        list_classes = list(df_sql_Classes['name'].values)

        #Переименовываем поле с названием модели из Excel - в 'name`
        for i in self.dict_xl_db_Fields:
            if self.dict_xl_db_Fields[i] == "name":
                self.xl_df_Products.rename(mapper={i: "name"}, axis='columns', inplace=True)

        exit_df = pd.DataFrame(columns=['fk_products', 'fk_classes'])

        for cls in list_classes:
            if cls in self.xl_df_Products.columns:
                ser_products_name = self.xl_df_Products[self.xl_df_Products[cls] == 1]['name']
                df_= pd.DataFrame(columns=['fk_products', 'fk_classes'])
                df_['fk_products'] = df_sql_Proucts[df_sql_Proucts['name'].isin(ser_products_name.values)]['id']
                cls0 = df_sql_Classes[df_sql_Classes['name'] == cls]['id']
                if cls0.empty:
                    df_['fk_classes'] = ""
                else:
                    df_['fk_classes'] = cls0.iloc[0]

                exit_df = pd.concat([exit_df, df_])

        return exit_df
# Insert & Delete MtM Products
    def MtM_Products_Classes_to_SQL(self):

        df_new = self.df_MtM_Products_Classes()
        df_old = self.Select_SQL_to_df(self.tbl_mtm_products_classes)

        df_join = df_old.merge(df_new, how="outer", on=['fk_products', 'fk_classes'], indicator=True)

        table_ = self.tbl_mtm_products_classes

        #delete
        df_to_delete = df_join[df_join['_merge'] == 'left_only'][['fk_products', 'fk_classes']]
        if not df_to_delete.empty:
            for i, row in df_to_delete.iterrows():
                delete_qry = table_.delete().\
                    where(table_.c.fk_products == row['fk_products']).\
                    where(table_.c.fk_classes == row['fk_classes'])
                self.connection.execute(delete_qry)

        #insert
        df_to_insert = df_join[df_join['_merge'] == 'right_only'][['fk_products', 'fk_classes']]
        if not df_to_insert.empty:
            self.Insert_df_to_SQL(df_to_insert, table_)

        print(df_join)

# Databse connect
    def DB_alchemy(self,
                   category,
                   db="mysql://shulya403:1qazxsw2@localhost/all_gid_2?charset=utf8mb4"):
        self.sql_engine = sql.create_engine(db, echo=True, encoding='utf8', convert_unicode=True)

        metadata = sql.MetaData(self.sql_engine)

        sql_tbl_name_products = category+'_products'
        sql_tbl_name_class = category + '_classes'
        sql_tbl_name_mtm_prod_class = category + '_products_has_nb_classes'
        sql_tbl_name_vardata = category + '_vardata'

        self.tbl_products = sql.Table(sql_tbl_name_products, metadata, autoload=True)
        self.tbl_classes = sql.Table(sql_tbl_name_class, metadata, autoload=True)
        self.tbl_mtm_products_classes = sql.Table(sql_tbl_name_mtm_prod_class, metadata, autoload=True)
        self.tbl_vardata = sql.Table(sql_tbl_name_vardata, metadata, autoload=True)

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

# Удаление df из таблцы по "name"
    def Delete_from_SQL(self, df, tbl):

        for i, row in df.iterrows():

            delete_qry = tbl.delete().where(tbl.c.name == row['name'])
            self.connection.execute(delete_qry)

# сопоставление двух df. новые по полю name
    def New_names(self, df_old, df_new):

        #Новые записи
        df_new.drop_duplicates(subset=['name'], keep='last', inplace=True)
        df_old_names = set(df_old['name'])
        df_new_names = set(df_new['name'])

        difference = df_new_names - df_old_names
        coincidence = df_old_names - difference
        old_to_delete = df_old_names - df_new_names

        exit_insert = df_new[df_new['name'].isin(difference)]

        #Проверка исправленнных

        df_old_names_restrict = df_old[df_new.columns]

        #exit_update = df_new.compare(df_old_names_restrict)
        exit_update = df_compare(df_old_names_restrict, df_new[df_new['name'].isin(coincidence)])

        exit_delete = df_old[df_old['name'].isin(old_to_delete)]

        return (exit_insert, exit_update, exit_delete)

# Products_handle
    def Products_to_SQL(self, df_new):

        tup_df = self.New_names(self.Select_SQL_to_df(self.tbl_products), df_new)
        df_select = tup_df[0]
        df_update = tup_df[1]

        if not df_select.empty:
            self.Insert_df_to_SQL(df_select, self.tbl_products)

        if not df_update.empty:
            self.Update_df_in_SQL(df_update, self.tbl_products)

# Classes_handle
    def Classes_to_SQL(self, df_new, delete_old=False):
        tup_df = self.New_names(self.Select_SQL_to_df(self.tbl_classes), df_new)
        df_select = tup_df[0]
        df_update = tup_df[1]

        if not df_select.empty:
            self.Insert_df_to_SQL(df_select, self.tbl_classes)

        if not df_update.empty:
            self.Update_df_in_SQL(df_update, self.tbl_classes)

        if delete_old:
            df_delete = tup_df[2]
            self.Delete_from_SQL(df_delete, self.tbl_classes)

    def Vardata_to_SQL(self, mth_list=[], update_old=False):

        now_y = str(dt.datetime.now().year)

        def add_0(x):
            if len(str(x)) == 1:
                return "0" + str(x)
            else:
                return str(x)



        if mth_list:
            mth_list = [now_y + "-" + add_0(x) + "-01" for x in mth_list]
            df_insert = self.df_Vardata[self.df_Vardata['month'].isin(mth_list)]
        else:
            df_insert = self.df_Vardata[self.df_Vardata['month'] != ""]
            mth_list = list(df_insert['month'].unique())

        df_products = self.Select_SQL_to_df(self.tbl_products)

        merge_ = df_insert.merge(df_products, how="left", left_on="product_name", right_on="name")
        print(merge_)
        df_insert.loc[:, 'fk_products'] = merge_['id'].values

        df_insert.dropna(subset=['fk_products'], inplace=True)
        df_insert.drop(['product_name'], axis='columns', inplace=True)

        df_old = self.Select_SQL_to_df(self.tbl_vardata)

        if update_old:

            date_mth_list = [dt.datetime.strptime(x, "%Y-%m-%d").date() for x in mth_list]
            df_delete = df_old[df_old['month'].isin(date_mth_list)]
            if not df_delete.empty:
                table_ = self.tbl_vardata
                for mth in df_delete['month'].unique():
                    print(mth)
                    delete_qry = table_.delete().where(table_.c.month == mth)
                    self.connection.execute(delete_qry)
            df_insert = df_insert[df_insert['month'].isin(mth_list)]
        else:
            old_months = {dt.date.strftime(x, "%Y-%m-%d") for x in df_old['month'].unique()}
            print(set(df_old['month'].unique()))
            new_months = set(mth_list) - old_months

            df_insert = df_insert[df_insert['month'].isin(new_months)]

        self.Insert_df_to_SQL(df_insert, self.tbl_vardata)


# Vardata to SQL



# MAIN

# def __init__ (self,
#                     xl_Products,
#                     xl_Vardata,
#                     dir_root = "C:\\Users\\shulya403\\Shulya403_works\\all_gid_2\\Data\\",
#                     Category='Nb',
#                     JSON_file="categories_fields.json"):

FillDB = DB_insert_from_excel(xl_Products="nb_models_07_update.xlsx",
                     xl_Vardata="NB_Report-5`20.xlsx",
                    Category="Nb")
FillDB.DB_alchemy(FillDB.Category)
FillDB.Products_to_SQL(df_new=FillDB.df_Products)
FillDB.Classes_to_SQL(df_new=FillDB.df_Classes, delete_old=True)
FillDB.MtM_Products_Classes_to_SQL()
#mth_list=[2, 4]
#FillDB.Vardata_to_SQL(mth_list=[], update_old=False)

