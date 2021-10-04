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
                if(isinstance(row[j], float)):
                    try:
                        str_row = str(int(row[j]))
                    except ValueError:
                        print(row["name"], j, row[j])
                        str_row = str(row[j])
                else:
                    str_row = str(row[j])

                if str(df_old[df_old['name'] == name][j].values[0]) != str_row:
                    print(name, df_old[df_old['name'] == name][j].values[0], str_row)
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
            df_ = df_[df_['name'].notna()]

            print("df_Products \n", df_.head())


            return df_
# Autochange
        def df_Autochange_Products(df, dict_fields):

            for i in dict_fields:
                print(i, dict_fields[i].keys())

                if dict_fields[i]['db_name'] == 'speed':
                    dict_fields[i]['db_name']
                    pass

                if "autochange" in dict_fields[i].keys():
                    if dict_fields[i]["autochange"]["part"]:
                        map_ = dict()
                        for j in df[dict_fields[i]['db_name']].unique():
                            for k in dict_fields[i]["autochange"]['change'].keys():
                                if str(k).lower() in str(j).lower():
                                    map_[j] = str(j).\
                                        replace(k, dict_fields[i]["autochange"]['change'][k]).\
                                        replace(k.title(), dict_fields[i]["autochange"]['change'][k])
                                    break
                                else:
                                    map_[j] = j
                    else:


                        map_ = dict_fields[i]["autochange"]['change']
                        for j in df[dict_fields[i]['db_name']].unique():

                            if not j in dict_fields[i]["autochange"]['change']:

                             map_[j] = j
                             for k in map_:
                                 if str(j).title() == str(k).title() and k != j:
                                     map_[j] = map_[k]
                                     break


                    df[dict_fields[i]['db_name']] = df[dict_fields[i]['db_name']].map(map_, na_action='ignore')
            return df

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
            drop_idx = df_[df_['sales_units'] == 0].index
            df_.drop(drop_idx, inplace=True)
            df_.fillna(0, inplace=True)

            return df_



# Собснна __init__
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
        self.df_Products = df_Autochange_Products(self.df_Products, dict_xl_Cat_Fields['Fields_products'])
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

        sql_tbl_name_products = category.lower() +  '_products'
        sql_tbl_name_class = category.lower()  + '_classes'
        sql_tbl_name_mtm_prod_class = category.lower()  + '_products_has_' + category.lower()  + '_classes'
        sql_tbl_name_vardata = category.lower()  + '_vardata'
        sql_tbl_name_shops_prices = category.lower()  + '_shops_prices'

        self.tbl_products = sql.Table(sql_tbl_name_products, metadata, autoload=True)
        self.tbl_classes = sql.Table(sql_tbl_name_class, metadata, autoload=True)
        self.tbl_mtm_products_classes = sql.Table(sql_tbl_name_mtm_prod_class, metadata, autoload=True)
        self.tbl_vardata = sql.Table(sql_tbl_name_vardata, metadata, autoload=True)
        self.tbl_shops_prices = sql.Table(sql_tbl_name_shops_prices, metadata, autoload=True)

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

    def Vardata_to_SQL(self, mth_list=[], update_old=False, now_y="2020"):

        if not now_y:
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
            print(set(df_old['month'].unique()))
            old_months = {dt.date.strftime(x, "%Y-%m-%d") for x in df_old['month'].unique()}
            print(set(df_old['month'].unique()))
            new_months = set(mth_list) - old_months
            print(new_months)

            df_insert = df_insert[df_insert['month'].isin(new_months)]

        self.Insert_df_to_SQL(df_insert, self.tbl_vardata)

class DB_insert_shops(DB_insert_from_excel):

    def __init__(self,
                 xl_Shops, #Месячные прайсы Filled
                 Category,
                 dir_root="../Data/",
                 #JSON_file="categories_fields.json"
                 drop_shops = ['yama']):

        def Check_Category(Category, df, filename):
            Cat_check = {
                "Nb": "Ноутбук",
                "Mnt": "Монитор"
            }
            cat_ = Cat_check[Category].lower()
            if df['Category'][0].lower() != cat_:
                print("В файле {} нет категории {}".format(filename, cat_.title()))
                raise

        self.Category = Category

        if dir_root:
            xl_filename = dir_root + Category + "/" + xl_Shops
        self.df_Shopprices = pd.read_excel(xl_filename, usecols=[
            'Category',
            'Date',
            'Modification_href',
            'Modification_name',
            'Vendor',
            'Modification_price',
            'Name',
            'Ok',
            'Site',
            'Vendor'
        ])

        Check_Category(Category, self.df_Shopprices, xl_Shops)
        set_sites = set(self.df_Shopprices['Site'].unique())
        set_sites = set_sites - set(drop_shops)
        self.df_Shopprices = self.df_Shopprices[
            (self.df_Shopprices['Ok'] == 1) &
            (self.df_Shopprices['Site'].isin(set_sites))].copy()

        self.DB_alchemy(self.Category)
        self.df_SQL_Products = self.Select_SQL_to_df(self.tbl_products)

    def df_Shops_Price(self):

        tbl_fld = {
            'Date': 'month',
            'Modification_href': 'modfication_href',
            'Modification_name': 'modification_name',
            'Modification_price': 'modification_price',
            'Site': 'shop_name',
            'Name': 'name'
        }
        df_ = self.df_Shopprices.rename(tbl_fld, axis='columns')


        df_.drop(columns=['Ok', 'Category', 'Vendor'], inplace=True)

        df_ = df_.merge(self.df_SQL_Products[['id', 'name']], how='inner', on='name')
        df_.rename({'id': 'fk_products_shop'}, axis='columns', inplace=True)

        return df_

    def To_DB_Shop_Price(self, erise_old=True):

        if erise_old:
            qry_delete = self.tbl_shops_prices.delete()
            self.connection.execute(qry_delete)

        self.Insert_df_to_SQL(self.df_Shops_Price(), self.tbl_shops_prices)

class Monitor_Models_Base_Update():
    def __init__(self, old_base, new_base, dir="C:\\Users\\User\\ITResearch\\all_gid_2\\Data\\Mnt\\", num=1):
        old_filename = dir + old_base
        new_filename = dir + new_base

        self.df_old = pd.read_excel(old_filename)
        self.df_new = pd.read_excel(new_filename)

        self.df_new = self.df_new[self.df_old.columns]

        self.df_old['name_low'] = self.df_old['Vendor'] + self.df_old['Model'].apply(lambda nm: str(nm).lower())
        self.df_new['name_low'] = self.df_new['Vendor'] + self.df_new['Model'].apply(lambda nm: str(nm).lower())

        self.num = num
        self.dir = dir


    def Concat_old_new(self, old, new):

        return pd.concat([old, new], ignore_index=True)

    def Drop_duplicates(self, df):
        df.drop_duplicates(subset=['name_low'], keep='last', inplace=True)
        df.drop(axis=1, columns=['name_low'], inplace=True)
        return df

    def Write_excel(self):

        df = self.Drop_duplicates(self.Concat_old_new(self.df_old, self.df_new))
        filename = self.dir + 'Monitors_Model_Base_' + str(max(list(df['Appear_month'].unique()))) + "-" + str(self.num) + ".xlsx"
        print(max(list(df['Appear_month'].unique())))

        df.to_excel(filename, index=False)

# MAIN

# def __init__ (self,
#                     xl_Products,
#                     xl_Vardata,
#                     dir_root = "C:\\Users\\shulya403\\Shulya403_works\\all_gid_2\\Data\\",C:/Users/User/ITResearch/all_gid_2/Data/
#                     Category='Nb',
#                     JSON_file="categories_fields.json"):



FillDB = DB_insert_from_excel(xl_Products="Mfp_Model_Base_08'2021-1.xlsx",
                      xl_Vardata="Mfp_Model_Base_08'2021-1.xlsx", #Менять месяцы на правильные согласно ctaiegoris_fields.json
                     Category="Mfp",
                    dir_root = "C:/Users/User/ITResearch/all_gid_2/Data/")
FillDB.DB_alchemy(FillDB.Category)
FillDB.Products_to_SQL(df_new=FillDB.df_Products)
FillDB.Classes_to_SQL(df_new=FillDB.df_Classes, delete_old=False)
FillDB.MtM_Products_Classes_to_SQL()
mth_list = [8]
FillDB.Vardata_to_SQL(mth_list=mth_list, update_old=True, now_y="2021")

# class DB_insert_shops(DB_insert_from_excel):
#     def __init__(self,
#                  xl_Shops, #Месячные прайсы Filled
#                  Category,
#                  dir_root="../Data/",
#                  drop_shops = ['yama']):

#Заполение магазинов для мониторов и ноутбуков

# FillShop = DB_insert_shops(
#                  xl_Shops="Ноутбук-Concat_Prices--Aug-21--Filled.xlsx", #Месячные прайсы Filled/Checked
#                  Category='Nb',
#                  dir_root="../Data/"
# )
#
# FillShop.To_DB_Shop_Price()


# Мониторы добавка и исправление моделей за месяц
#
# class Monitor_Models_Base_Update():
#     def __init__(self, old_base, new_base, dir="C:\\Users\\User\\ITResearch\\all_gid_2\\Data\\Mnt\\", num=1):

# July_monitors = Monitor_Models_Base_Update("Monitors_Model_Base_2021_07-1.xlsx",
#                                            "Allgid monitors august 2021.xlsx",
#                                            dir="C:/Users/User/ITResearch/all_gid_2/Data/Mnt/")
# July_monitors.Write_excel()
