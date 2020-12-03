#TODO:
# Форма в кнопках
# Кнопка новинки
#  Кнопка все актуальные новинки
#Декоратор для цен с разделителями
#Шаблон для выдачи десятки со средней ценой (транспонированная таблица)
#Выбор полей для отображения из числа ТТХ (using)
#взять сджойниную таблицу products-vardata отбор по фильтру classes и по дате, отсортировать, взять топ
#Выдать цену по двум последним месяцам


from django.shortcuts import render
#from django.views.generic import View, DetailView, TemplateView
from django.http import HttpResponse
from .models import MntClasses, \
    MntProductsHasMntClasses, \
    MntVardata, \
    MntProducts,\
    NbClasses, \
    NbProducts, \
    NbProductsHasNbClasses, \
    NbVardata,\
    MfpClasses,\
    MfpProducts,\
    MfpProductsHasMfpClasses,\
    MfpVardata,\
    MfpShopsPrices,\
    MntShopsPrices,\
    NbShopsPrices,\
    TextLinks

from datetime import datetime as dt
#from datetime import date
import django_pandas as pd
from django_pandas.io import read_frame


#from django import forms
from pprint import pprint
from django.db.models import Count, F, Sum, Avg, Q

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def digit_separator(digit):
    if digit:
        try:
            str_digit = str(int(digit))
        except ValueError:
            return 'n/a'
        exit_ = str()
        tail = len(str_digit) % 3
        for i in range(len(str_digit)-3, -1, -3):
            exit_ = " " + str_digit[i:i+3] + exit_

        if tail != 0:
            exit_ = str_digit[:tail] + exit_
            return exit_
        else:
            return exit_[1:]
    else:
        return digit

@register.filter
def sort_keys(keys):

    return sorted(list(keys))



dict_categories = {
        'Mnt': {
            'category_name': "Мониторы",
            'db_tables':    {
                'products': MntProducts,
                'classes': MntClasses,
                'mtm_prod_clas': MntProductsHasMntClasses,
                'vardata': MntVardata,
                'shop_prices': MntShopsPrices

            },
            'fields_show': {

                    'brand': {
                        "html_name": "Компания",
                        "id": 0,
                        "short": False
                    },

                    'name': {
                        "html_name": "Модель",
                        "id": 1,
                        "short": False
                    },
                    'type': {
                        "html_name": "Экран",
                        "id": 2,
                        "short": True
                    },
                    'curved': {
                        "html_name": "Изогнутый",
                        "id": 4,
                        "short": True
                    },
                    'game': {
                        "html_name": "Игровой",
                        "id": 3,
                        "short": True
                    }
            }
        },
        'Nb': {
            'category_name': "Ноутбуки",
            'db_tables':    {
                'products': NbProducts,
                'classes': NbClasses,
                'mtm_prod_clas': NbProductsHasNbClasses,
                'vardata': NbVardata,
                'shop_prices': NbShopsPrices
            },
            'fields_show': {

                    'brand': {
                        "html_name": "Компания",
                        "id": 0,
                        "short": False
                    },
                    'name': {
                        "html_name": "Модель",
                        "id": 1,
                        "short": False
                    },
                    'screen_size': {
                        "html_name": "Экран",
                        "id": 2,
                        "short": True
                    },
                    'cpu_vendor': {
                        "html_name": "Произв. процессора",
                        "id": 3,
                        "short": True
                    },
                    'base_platform': {
                        "html_name": "Поколение процессора",
                        "id": 4,
                        "short": False
                    },
                    'gpu_list': {
                        "html_name": "Графика",
                        "id": 5,
                        "short": True
                    },
                    'appear_month': {
                        "html_name": "Начало продаж",
                        "id": 6,
                        "short": False
                    }
            }
        },
        'Mfp': {
            'category_name': "Принтеры и МФУ",
            'db_tables': {
                'products': MfpProducts,
                'classes': MfpClasses,
                'mtm_prod_clas': MfpProductsHasMfpClasses,
                'vardata': MfpVardata,
                'shop_prices': MfpShopsPrices
            },
            'fields_show': {

                'brand': {
                        "html_name": "Компания",
                        "id": 0,
                        "short": False
                    },
                'name': {
                        "html_name": "Модель",
                        "id": 1,
                        "short": False
                    },
                'type': {
                        "html_name": "",
                        "id": 2,
                        "short": True
                    },
                'prt_technology': {
                        "html_name": "Печать",
                        "id": 3,
                        "short": True
                    },
                'color': {
                        "html_name": "Цвет",
                        "id": 4,
                        "short": True
                    },
                'format_a': {
                        "html_name": "Формат",
                        "id": 5,
                        "short": True
                    },
                'photo': {
                        "html_name": "Фотопринтер",
                        "id": 6,
                        "short": True
                    }
                }
            }

       }

cat_def = ""
category = dict()
db_tbl = dict()
categories_list = list()
dict_sorted_fields_show = dict()
dict_fields_short_show = dict()


# Формирование вложенного словаря по таблице _classes
def Dict_by_Classes(query):

    def nested_dict(query):
        dict_ = dict()
        subtypes = query.values_list('class_subtype').distinct().order_by('class_subtype')
        for i in subtypes:
            dict_[i[0]] = list(query.filter(class_subtype__exact=i[0]).values('name', 'text', 'explanation'))

        return dict_

    dict_ = {}
    dict_['CL'] = dict()
    cl_query = query.filter(type__exact="CL")
    dict_['CL'] = nested_dict(cl_query)

    dict_['GO'] = dict()
    go_query = query.filter(type__exact="GO")

    dict_['GO'] = nested_dict(go_query)

    return dict_

def Dict_by_Classes2():

    global db_tbl, list_enabled

    def Dict_class_subtype(cl_type, qry_classes):
        exit_sub_ = dict()
        qry_subtype = qry_classes.filter(type=cl_type)
        for sub_type in vlist_to_list(qry_subtype.values_list('class_subtype').distinct()):
            if not sub_type:
                st_name = '1'
            else:
                st_name= sub_type
            exit_sub_[st_name] = qry_subtype.filter(class_subtype=sub_type).values('name', 'explanation', 'text')

        return exit_sub_
    exit_ = dict()
    qry_classes = db_tbl['classes'].objects.all()
    list_enabled = vlist_to_list(qry_classes.values_list('name'))
    for cl_type in vlist_to_list(qry_classes.values_list('type').distinct()):
        exit_[cl_type] = Dict_class_subtype(cl_type, qry_classes)

    return exit_

def vlist_to_list(vlist):
    return [i[0] for i in vlist]

# Получение выборки из mtm только с продуктами встр. в отфильтрованных формой классах
def Get_Products_Mtm(post_return, db_tbl):

    # joined_mtm - выборка из mtm по отфильтрованным классам
    joined_mtm = db_tbl['mtm_prod_clas'].objects \
        .filter(fk_classes__name__in=post_return) \
        .values('fk_products', 'fk_classes')

    # inner_join_products число упоминаний продуктов в отфильтрованной таблице mtm
    inner_join_products = joined_mtm.values('fk_products') \
        .annotate(Count('fk_products'))
    pprint(inner_join_products)
    # inner_join_products_ - только продукты из inner_join встр в количестве классов равном числу отдачи формы
    inner_join_products_ = inner_join_products \
        .filter(fk_products__count=len(post_return)) \
        .values_list('fk_products')
    pprint(inner_join_products_)

    # products_mtm - список записей в mtm с продуктом присутсв. во всех отфильтрованных классах
    products_mtm = db_tbl['mtm_prod_clas'].objects \
        .filter(fk_products__in=inner_join_products_) \
        .order_by('fk_products') \
        .values('fk_products', 'fk_classes')

    return products_mtm

# выборка из базы

def Init_cat(cat_):

    global categories_list, category, db_tbl, cat_def, dict_sorted_fields_show, dict_fields_short_show, new_form

    cat_def = cat_
    category = dict_categories[cat_def]
    db_tbl = category['db_tables']
    categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    dict_sorted_fields_show = {k: v['html_name'] for k, v in
                               sorted(category['fields_show'].items(), key=lambda id: id[1]["id"])}
    dict_fields_short_show = {k: v for k, v in dict_sorted_fields_show.items() if category['fields_show'][k]['short'] == True}

    new_form = Dict_by_Classes2()


form_return = []
products_for_execute = []
df_data = None


def page_Category_Main(request, cat_):

    global categories_list, \
        category, \
        db_tbl, \
        cat_def, \
        dict_sorted_fields_show, \
        products_for_execute, \
        form_return, \
        new_form, \
        list_enabled, \
        period_mth_rus, \
        period_inbase, \
        df_data, \
        enabled_return

    if (cat_ != cat_def):
        Init_cat(cat_)

    #category = dict_categories[cat_]
    #db_tbl = category['db_tables']

    #categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    #form_fld = db_tbl['classes'].objects.all()
    #new_form = Dict_by_Classes2()
    #list_enabled = vlist_to_list(list(form_fld.values_list('name')))

    if request.POST:
        #pprint(request.POST)
        post_return = list(request.POST.keys())
        post_return.remove('csrfmiddlewaretoken')
        form_return = post_return

        products_mtm = Get_Products_Mtm(post_return, db_tbl)

        # products_for_execute - list id отфильторванных моделей
        products_for_execute = vlist_to_list(list(products_mtm.values_list('fk_products').distinct()))

        # classes_for_execute - list id доступных после фильтра классов
        classes_for_execute = vlist_to_list(list(products_mtm.values_list('fk_classes').distinct()))

        #print(products_for_execute)
        list_enabled_ = db_tbl['classes'].objects.filter(id__in=classes_for_execute).values_list('name')
        list_enabled_ = vlist_to_list(list(list_enabled_))
        #print(list_enabled_)
        if list_enabled_:
            enabled_return = list_enabled_
        else:
            enabled_return = list_enabled

    else:
        post_return = []
        enabled_return = list_enabled
        joined_mtm = "пусто"

        products_for_execute = []

    df_data = Get_Sales_Top(products_for_execute, timelag=2)
    if len(df_data) > 0:
        tab_novelty = df_data[df_data['appear_month'].isin(period_inbase)].sort_values('brand_name').to_dict()

        q_data = len(df_data)

        if q_data >= 20:
            tab_marketability = df_data[:20].sort_values('price_avg').to_dict()
        else:
            tab_marketability = df_data.to_dict()
    else:
        tab_marketability = dict()
        tab_novelty = dict()

    best_links = Get_Bestsellers_links(cat_)

    exit_ = {
        'category_name':  category['category_name'],
        'categories_list': categories_list,
        'action': cat_,
        'tbl_ttx_col': [x for x in tab_marketability.keys() if x not in ['id', 'brand_name', 'price_avg', 'appear_month']],
        'tbl_data': tab_marketability,
        'tbl_data_nov': tab_novelty,
        'new_form': new_form,
        'enabled': enabled_return,
        'checked_items': post_return,
        'period': period_mth_rus,
        'bestesellers_links': best_links
    }

    return render(request, template_name="category.html", context=exit_)

def page_Product(request, cat_, product_):

    global form_return, products_for_execute, db_tbl, categories_list, new_form, df_data

    if not db_tbl:
        Init_cat(cat_)

    #таблица ТТХ

    Product = db_tbl['products'].objects.filter(id__iexact=product_).values()

    fields_ = list(Product[0].keys())

    dict_ttx = dict()
    dict_html_names = Fld_html_names(fields_, cat_, ['brand', 'name', 'id'])
    for i in fields_:
        if i not in ['brand', 'name', 'id']:
            dict_ttx[dict_html_names[i]] = Product[0][i]


    shop_mod = Get_Shops(product_)
    try:
        if not df_data.empty:
            df_ = df_data.sort_values('brand_name').to_dict()
        else:
            df_ = dict()
    except:
        df_ = dict()



    exit_ = {
        'categories_list': categories_list,
        'vendor': Product[0]['brand'],
        'name': Product[0]['name'],
        'ttx': dict_ttx,
        'new_form': new_form,
        'checked_items': form_return,
        'tbl_data': df_,
        'shop_mod': shop_mod,
        'action': cat_,
        'other_products': df_data,

    }

    return render(request, template_name="product.html", context=exit_)

def Fld_html_names(fields_, cat_, not_change=[]):

    exit_ = dict()
    for i in fields_:
        if i not in not_change:
            try:
                exit_[i] = dict_categories[cat_]['fields_show'][i]['html_name']
            except KeyError:
                exit_[i] = i

    return exit_

def Get_Prod_Execute_join_vardata(list_products, qry_period):

    global db_tbl, cat_def

    sales_sum = cat_def.lower() + "vardata__sales_units"
    filter_months = {
        cat_def.lower() + "vardata__month__in": qry_period
    }
    price_avg = cat_def.lower() + "vardata__price_rur"
    qry_total_execute = db_tbl['products'].objects.\
        filter(id__in=list_products).\
        annotate(sales_sum=Sum(sales_sum, filter=Q(**filter_months)),
                 price_avg=Avg(price_avg, filter=Q(**filter_months))).exclude(sales_sum__isnull=True)

    return qry_total_execute

def months_names(period_):
    mth_names = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь'
        }

    exit_ = list()
    for i in period_:
        exit_.append(mth_names[i.month])


    return exit_

def Get_Period_inbase(timelag):

    global db_tbl, period_mth_rus, period_inbase

    period_inbase = vlist_to_list(db_tbl['vardata'].objects.values_list('month').distinct().order_by())
    if None in period_inbase:
            period_inbase.remove(None)
    if len(period_inbase) < timelag:
         timelag=len(period_inbase)

    period_inbase = period_inbase[-timelag:]

    period_mth_rus = months_names(period_inbase)


    return period_inbase


def Get_Sales_Top(list_products, timelag=2):

    global db_tbl, dict_fields_short_show

    if None in list_products:
        list_products.remove(None)

    now = int(dt.strftime(dt.now(), "%m"))

    if list_products:
        total_ = Get_Prod_Execute_join_vardata(list_products, Get_Period_inbase(timelag))
    else:
        all_ = vlist_to_list(db_tbl['vardata'].objects.values_list('fk_products').distinct())
        total_ = Get_Prod_Execute_join_vardata(all_, Get_Period_inbase(timelag))
    if total_:

        df = read_frame(total_.order_by("-sales_sum"))
        fix_fields = {'id', 'brand', 'name', 'price_avg', 'appear_month'}
        for i in df.columns:
            if i not in fix_fields:
                if i not in set(dict_fields_short_show.keys()):
                    df.drop(i, axis='columns', inplace=True)
        rename_ttx = {k: v for k, v in dict_fields_short_show.items() if k not in fix_fields}
        df['brand_name'] = df['brand'] + ' ' + df['name']
        df.drop(['brand', 'name'], axis='columns', inplace=True)
        df.rename(rename_ttx, axis='columns', inplace=True)

        exit_ = df

    else:
        exit_ = []

    return exit_

def Get_Shops(product_):
    global db_tbl

    product_in_shops = db_tbl['shop_prices'].objects.\
            filter(fk_products_shop=product_).order_by('modification_price')

    return product_in_shops

def Get_Bestsellers_links(cat):

    qry = TextLinks.objects.all().order_by('-date')[:10]

    return qry



