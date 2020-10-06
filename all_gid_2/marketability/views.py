#TODO:
#Магазины
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
    NbShopsPrices\

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
    str_digit = str(int(digit))
    exit_ = str()
    tail = len(str_digit) % 3
    for i in range(len(str_digit)-3, -1, -3):
        exit_ = " " + str_digit[i:i+3] + exit_

    if tail != 0:
        exit_ = str_digit[:tail] + exit_
        return exit_
    else:
        return exit_[1:]



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
                        "short": True
                    },
                    'gpu_list': {
                        "html_name": "Графика",
                        "id": 5,
                        "short": True
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
                        "html_name": "Тех-ия печати",
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

#формирование html формы руками
def Form_by_dict_classes(dict, post, enabled, first=True):

    def td_type(dict_type):
        str_ = ""
        for i in dict_type:
            if i != "":
                str_ += "<b>{}</b><br>".format(i)
            for j in dict_type[i]:
                if j['name'] in post:
                    chk = "checked"
                else:
                    chk = ""
                if j['name'] in enabled:
                    disabled = ""
                    del_label = ("", "",)
                else:
                    disabled = "disabled"
                    del_label = ("<del>", "</del>",)
                str_input = "<input type=\"checkbox\" name=\"{}\" {} id=\"{}\" value=\"Yes\" {}>"\
                    .format(j['name'], chk, j['name'], disabled)
                str_input +="{}<label for=\"{}\">{}</label><br>{}".format(del_label[0], j['name'], j['text'], del_label[1])
                if j['explanation']:
                    str_input += "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<i>" + j['explanation'] + "</i><br>"
                str_ += str_input
            str_ += "<br>"

        return str_

    str_header = "<table><tr>"
    str_CL = "<td valign=\"top\">" + td_type(dict['GO']) + "</td>"
    str_GO = "<td valign=\"top\">" + td_type(dict['CL']) + "</td>"
    str_footer = "</tr></table>"

    exit_ = str_header + str_CL + str_GO + str_footer

    with open("marketability/patterns/form.html", 'w', encoding='utf-8') as f:
        f.write(exit_)


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

    global categories_list, category, db_tbl, cat_def, dict_sorted_fields_show, dict_fields_short_show

    cat_def = cat_
    category = dict_categories[cat_def]
    db_tbl = category['db_tables']
    categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    dict_sorted_fields_show = {k: v['html_name'] for k, v in
                               sorted(category['fields_show'].items(), key=lambda id: id[1]["id"])}
    dict_fields_short_show = {k: v for k, v in dict_sorted_fields_show.items() if category['fields_show'][k]['short'] == True}

form_return = []
products_for_execute = []


def page_Category_Main(request, cat_):

    global categories_list, \
        category, \
        db_tbl, \
        cat_def, \
        dict_sorted_fields_show, \
        products_for_execute, \
        form_return

    if (cat_ != cat_def):
        Init_cat(cat_)

    #category = dict_categories[cat_]
    #db_tbl = category['db_tables']

    #categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    form_fld = db_tbl['classes'].objects.all()
    list_enabled = vlist_to_list(list(form_fld.values_list('name')))

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

        # tbl_joined = {"1": 0, "2": 0} ???
        #list_products = db_tbl['products'].objects.filter(id__in=products_for_execute).values('name')
        #pprint(list_products)
    else:
        post_return = []
        enabled_return = list_enabled
        joined_mtm = "пусто"
        #tbl_joined = {"1": 0, "2": 0}
        #list_products = []
        products_for_execute = []

    tab_marketability = Get_Sales_Top(products_for_execute, q=10)

    #html.формы вызывается шаблоном из include
    dict_form_fld = Dict_by_Classes(form_fld)
    Form_by_dict_classes(dict_form_fld, post_return, enabled_return)

    pass
    exit_ = {
        'category_name':  category['category_name'],
        'categories_list': categories_list,
        'action': cat_,
        'tbl_ttx_col': [x for x in tab_marketability.keys() if x not in ['id', 'brand_name', 'price_avg']],
        'tbl_data': tab_marketability

    }

    return render(request, template_name="category.html", context=exit_)

def page_Product(request, cat_, product_):

    global form_return, products_for_execute, db_tbl, categories_list

    if not db_tbl:
        Init_cat(cat_)

    Product = db_tbl['products'].objects.filter(id__iexact=product_).values()

    fields_ = list(Product[0].keys())
    dict_ttx = dict()
    for i in fields_:
        if i not in ['brand', 'name', 'id']:
            dict_ttx[i] = Product[0][i]


    Filters = db_tbl['classes'].objects.filter(name__in=form_return).\
        values('type', 'text')
    filter_GO = list()
    filter_CL = list()
    if Filters:
        for i in Filters:
            if i['type'] == 'GO':
                filter_GO.append(i['text'])
            elif i['type'] == 'CL':
                filter_CL.append(i['text'])

    list_Products_filter = db_tbl['products'].objects.\
                    filter(id__in=products_for_execute).\
                    values('brand', 'name', 'id')

    pprint(list_Products_filter)

    #Нужен ли здесь класс?
    class FProducts(object):
        def __init__(self, id, brand, name):

            self.id = str(id),
            self.brand = str(brand),
            self.name = str(name)

            self.id = self.id[0]
            self.brand = self.brand[0]

            print(self.id, self.brand, self.name)

    fproducts = list()
    for i in list(list_Products_filter):
        fproducts.append(FProducts(id=i['id'], brand=i['brand'], name=i['name']))

    shop_mod = Get_Shops(product_)


    exit_ = {
        'categories_list': categories_list,
        'vendor': Product[0]['brand'],
        'name': Product[0]['name'],
        'ttx': dict_ttx,
        'filter_GO': filter_GO,
        'filter_CL': filter_CL,
        'fproducts': fproducts,
        'shop_mod': shop_mod,
        'action': cat_
    }
    return render(request, template_name="product.html", context=exit_)

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
                 price_avg=Avg(price_avg, filter=Q(**filter_months)))

    return qry_total_execute

def Get_Period_inbase(timelag):

    global db_tbl

    period_inbase = vlist_to_list(db_tbl['vardata'].objects.values_list('month').distinct().order_by())
    if None in period_inbase:
            period_inbase.remove(None)
    if len(period_inbase) < timelag:
         timelag=len(period_inbase)

    period_inbase = period_inbase[-timelag:]

    return period_inbase


def Get_Sales_Top(list_products, timelag=2, q=5):

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

        df = read_frame(total_.order_by("-sales_sum")[:q])
        fix_fields = {'id', 'brand', 'name', 'price_avg'}
        for i in df.columns:
            if i not in fix_fields:
                if i not in set(dict_fields_short_show.keys()):
                    df.drop(i, axis='columns', inplace=True)
        rename_ttx = {k: v for k, v in dict_fields_short_show.items() if k not in fix_fields}
        df['brand_name'] = df['brand'] + ' ' + df['name']
        df.drop(['brand', 'name'], axis='columns', inplace=True)
        df.rename(rename_ttx, axis='columns', inplace=True)

        exit_ = df.to_dict()

    else:
        exit_ = []

    return exit_

def Get_Shops(product_):
    global db_tbl

    product_in_shops = db_tbl['shop_prices'].objects.\
            filter(fk_products_shop=product_).order_by('modification_price')

    return product_in_shops



