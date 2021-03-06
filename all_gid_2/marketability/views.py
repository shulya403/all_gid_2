from django.shortcuts import render
#from django.views.generic import View, DetailView, TemplateView
#from django.http import HttpResponse
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
from datetime import date
import django_pandas as pd
import pandas as pdd
from django_pandas.io import read_frame
from django.db.models import Count, F, Sum, Avg, Q

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_value(dictionary, key):
    return dictionary[key]

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

def DB_table(cat_):
    ORM_Models_names = {
    'Mnt': {
            'products': MntProducts,
            'classes': MntClasses,
            'mtm_prod_clas': MntProductsHasMntClasses,
            'vardata': MntVardata,
            'shop_prices': MntShopsPrices
            },

    'Nb': { 'products': NbProducts,
            'classes': NbClasses,
            'mtm_prod_clas': NbProductsHasNbClasses,
            'vardata': NbVardata,
            'shop_prices': NbShopsPrices
        },

    'Mfp': {'products': MfpProducts,
            'classes': MfpClasses,
            'mtm_prod_clas': MfpProductsHasMfpClasses,
            'vardata': MfpVardata,
            'shop_prices': MfpShopsPrices
        },

    }

    return ORM_Models_names[cat_]

def Dict_tabs_page_form():
    dict_tabs = {
        'marketability': {"rus_name": "ПОПУЛЯРНЫЕ",
                          "img_active": "Star white-1.svg",
                          "img_noactive": "Star gray.svg"},
        'novelity': {"rus_name": "НОВИНКИ",
                     "img_active": "Gray white.svg",
                     "img_noactive": "Lamp gray-1.svg"}
    }

    return dict_tabs

#Опредление категории
def Init_cat(request, cat_, db_tbl):
    dict_categories = {
        'Mnt': {
            'category_name': "Мониторы",

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
                    "html_name": "Вогнутый  ",
                    "id": 4,
                    "short": True
                },
                'game': {
                    "html_name": "Игровой",
                    "id": 3,
                    "short": True
                }
            },
            'timelag': 2
        },
        'Nb': {
            'category_name': "Ноутбуки",

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
            },
            'timelag': 2
        },
        'Mfp': {
            'category_name': "Принтеры и МФУ",

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
                    "html_name": "Тип",
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
            },
            'timelag': 1
        }
    }

    if cat_:
        request.session['cat_'] = cat_

        category = dict_categories[cat_]

        request.session['categories_list'] = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

        #request.session['db_tbl'] = category['db_tables']
        #db_tbl = DB_table(cat_)

        request.session['cat_rus_name'] = category['category_name']

        request.session['dict_sorted_fields_show'] = {k: v['html_name'] for k, v in
                                   sorted(category['fields_show'].items(), key=lambda id: id[1]["id"])}

        request.session['dict_fields_short_show'] = {k: v for k, v in request.session['dict_sorted_fields_show'].items() if category['fields_show'][k]['short'] == True}

        request.session['new_form'] = Dict_by_Classes2(request, db_tbl)

        request.session['enabled_return'] = request.session['list_enabled']

        request.session['tab_active'] = 'marketability'

        request.session['timelag'] = category['timelag']

        request.session['form_return'] = []

    else:
        request.session['categories_list'] = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

        request.session['cat_'] = cat_

        category = dict_categories[cat_]

        request.session['categories_list'] = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    return category

# Формирование вложенного словаря по таблице _classes
def Dict_by_Classes2(request, db_tbl):

    def Dict_class_subtype(cl_type, qry_classes):
        exit_sub_ = dict()
        qry_subtype = qry_classes.filter(type=cl_type)
        for sub_type in vlist_to_list(qry_subtype.values_list('class_subtype').distinct()):
            if not sub_type:
                st_name = '1'
            else:
                st_name = sub_type
            exit_sub_[st_name] = list()
            for cls in qry_subtype.filter(class_subtype=sub_type).values('name', 'explanation', 'text'):
                exit_sub_[st_name].append(cls)

        return exit_sub_

    exit_ = dict()
    qry_classes = db_tbl['classes'].objects.all()

    request.session['list_enabled'] = vlist_to_list(qry_classes.values_list('name'))

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

    # inner_join_products_ - только продукты из inner_join встр в количестве классов равном числу отдачи формы
    inner_join_products_ = inner_join_products \
        .filter(fk_products__count=len(post_return)) \
        .values_list('fk_products')


    # products_mtm - список записей в mtm с продуктом присутсв. во всех отфильтрованных классах
    products_mtm = db_tbl['mtm_prod_clas'].objects \
        .filter(fk_products__in=inner_join_products_) \
        .order_by('fk_products') \
        .values('fk_products', 'fk_classes')

    return products_mtm


def page_Category_Main(request, cat_):

    #Обновление параметров категории - даннае для формы и прочее
    db_tbl = DB_table(cat_)

    try:
        if cat_ != request.session['cat_']:
            category = Init_cat(request, cat_, db_tbl)

    except KeyError:
        category = Init_cat(request, cat_, db_tbl)

    #dict_sorted_fields_show = request.session['dict_sorted_fields_show']
    new_form = request.session['new_form']
    list_enabled = request.session['list_enabled']
    #timelag = request.session['timelag']
    #period_inbase = request.session['period_inbase']
    category_name = request.session['cat_rus_name']
    categories_list = request.session['categories_list']
    tab_active = request.session['tab_active']
    tab_data = Dict_tabs_page_form()
    tab_list = list(tab_data.keys())

    if request.POST:
        post_return = list(request.POST.keys())
        tab_active = request.POST['tabs']
        post_return.remove('csrfmiddlewaretoken')
        post_return.remove('tabs')

        request.session['form_return'] = post_return

        products_mtm = Get_Products_Mtm(post_return, db_tbl)

        # products_for_execute - list id отфильторванных моделей
        products_for_execute = vlist_to_list(list(products_mtm.values_list('fk_products').distinct()))

        request.session['products_for_execute'] = products_for_execute

        # classes_for_execute - list id доступных после фильтра классов
        classes_for_execute = vlist_to_list(list(products_mtm.values_list('fk_classes').distinct()))

        #print(products_for_execute)
        list_enabled_ = db_tbl['classes'].objects.filter(id__in=classes_for_execute).values_list('name')
        list_enabled_ = vlist_to_list(list(list_enabled_))
        #print(list_enabled_)
        if list_enabled_:
            request.session['enabled_return'] = list_enabled_
        else:
            request.session['enabled_return'] = list_enabled

        enabled_return = request.session['enabled_return']

    else:
        post_return = request.session['form_return']
        #request.session['enabled_return'] = list_enabled
        enabled_return = request.session['enabled_return']

        if post_return:
            pass
        else:
            request.session['products_for_execute'] = []

        #products_for_execute = request.session['products_for_execute']

    period_inbase = Get_Period_inbase(request, db_tbl)
    period = request.session['period_mth_rus']

    df_data = Get_Sales_Top(request, db_tbl, period_inbase)

    request.session['dict_df_data'] = df_data[['id', 'brand', 'name', 'price_avg']].to_dict()

    if len(df_data) > 0:
        tab_novelty = df_data[df_data['appear_month'].isin(period_inbase)].sort_values('price_avg').to_dict()

        q_data = len(df_data)

        if q_data >= 20:
            tab_marketability = df_data[:20].sort_values('price_avg').to_dict()
        else:
            tab_marketability = df_data.sort_values('price_avg').to_dict()
    else:
        tab_marketability = dict()
        tab_novelty = dict()

    best_links = Get_Bestsellers_links()

    exit_ = {
        'category_name':  category_name,
        'categories_list': categories_list,
        'action': cat_,
        'tbl_ttx_col': [x for x in tab_marketability.keys() if x not in ['id', 'brand', 'name', 'price_avg', 'appear_month']],
        'tbl_data': tab_marketability,
        'tbl_data_nov': tab_novelty,
        'new_form': new_form,
        'enabled': enabled_return,
        'checked_items': post_return,
        'period': period,
        'bestesellers_links': best_links,
        'tab_active': tab_active,
        'tab_list': tab_list,
        'tab_data': tab_data
    }

    return render(request, template_name="al_category.html", context=exit_)

def page_Product(request, cat_, product_):

    db_tbl = DB_table(cat_)

    try:
        if request.session['cat_'] == cat_:
            pass
        else:
            category = Init_cat(request, cat_, db_tbl)
    except KeyError:
        category = Init_cat(request, cat_, db_tbl)

    new_form = request.session['new_form']
    form_return = request.session['form_return']
    #list_enabled = request.session['list_enabled']
    timelag = request.session['timelag']
    #period = request.session['period_mth_rus']
    category_name = request.session['cat_rus_name']
    categories_list = request.session['categories_list']
    #tab_active = request.session['tab_active']
    tab_data = Dict_tabs_page_form()
    #tab_list = list(tab_data.keys())

    try:
        if request.session['products_for_execute']:
            pass

        df_data = pdd.DataFrame(request.session['dict_df_data'])

    except KeyError:
        request.session['enabled_return'] = request.session['list_enabled']
        #enabled_return = request.session['enabled_return']

        request.session['products_for_execute'] = []
        products_for_execute = request.session['products_for_execute']

        df_data = Get_Sales_Top(products_for_execute, tab_data, Get_Period_inbase(request, tab_data))

    Product = None
    while not Product:
        Product = db_tbl['products'].objects.filter(id__iexact=product_).values()

    fields_ = list(Product[0].keys())

    list_this_classes = Get_This_Classes(product_, db_tbl)
    this_classes = db_tbl['classes'].objects.filter(id__in=list_this_classes)

    miscell_products, len_miscell = Get_Miscell_Products(product_, set(vlist_to_list(list_this_classes)), df_data, db_tbl)

    dict_ttx = dict()
    dict_html_names = Fld_html_names(request, fields_, ['brand', 'name', 'id'])
    for i in fields_:
        if i not in ['brand', 'name', 'id']:
            dict_ttx[dict_html_names[i]] = Product[0][i]

    q_data = len(df_data)
    if q_data >= 20:
        top20 = df_data[:20][['id', 'brand', 'name', 'price_avg']].sort_values('price_avg').to_dict('records')
    else:
        top20 = df_data[['id', 'brand', 'name', 'price_avg']].sort_values('price_avg').to_dict('records')

    shop_mod = Get_Shops(request, db_tbl, product_)

    exit_ = {
        'category_name': category_name,
        'categories_list': categories_list,
        'vendor': Product[0]['brand'],
        'name': Product[0]['name'],
        'ttx': dict_ttx,
        'new_form': new_form,
        'checked_items': form_return,
        'shop_mod': shop_mod,
        'action': cat_,
        'top_products': top20,
        'this_price': df_data[df_data['name'] == Product[0]['name']]['price_avg'].values,
        'miscell': miscell_products,
        'len_miscell': len_miscell,
        'this_classes': this_classes

    }

    return render(request, template_name="al_product.html", context=exit_)

#Список классов конкретного продукта
def Get_This_Classes(product_, db_tbl):

    return db_tbl['mtm_prod_clas'].objects.filter(fk_products=product_).values_list('fk_classes')

#Список продуктов с идентичным набором классов что и у данного продукта
def Get_Miscell_Products(product_, set_this_classes, df_data, db_tbl):

    list_df_data = df_data['id'].to_list()


    qry_miscell = db_tbl['mtm_prod_clas'].objects.filter(fk_products__in=list_df_data).\
        values('fk_products').distinct().annotate(fcl = F('fk_classes'))
    dict_miscell = dict()
    for fpr in qry_miscell:
        try:
            dict_miscell[fpr['fk_products']].add(fpr['fcl'])
        except Exception:
            dict_miscell[fpr['fk_products']] = {fpr['fcl']}

    products_miscell = list()
    for i in dict_miscell:
        if dict_miscell[i] == set_this_classes:
            products_miscell.append(i)

    df_miscell = df_data[df_data['id'].isin(products_miscell)]
    df_miscell_vendor = df_miscell[['brand', 'id', 'name', 'price_avg']].groupby('brand')
    agg_miscell_vendor = df_miscell_vendor[['id', 'name', 'price_avg']].agg(list)

    dict_miscell_vendor = dict()
    for i, row in agg_miscell_vendor.iterrows():
        list_name_price = list()

        q = len(row['name'])
        for j in range(q):
            list_name_price.append({'id': row['id'][j], 'name': row['name'][j], 'price': row['price_avg'][j]})

        dict_miscell_vendor[i] = list_name_price

    return dict_miscell_vendor, len(df_miscell)


def Fld_html_names(request, fields_, not_change=[]):

    exit_ = dict()
    for i in fields_:
        if i not in not_change:
            try:
                exit_[i] = request.session['dict_sorted_fields_show'][i]
            except KeyError:
                exit_[i] = i

    return exit_

def Get_Prod_Execute_join_vardata(request, db_tbl, list_products, qry_period):

    cat_def = request.session['cat_']

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

def Get_Period_inbase(request, db_tbl):

    timelag = request.session['timelag']

    period_inbase = vlist_to_list(db_tbl['vardata'].objects.values_list('month').distinct().order_by())
    if None in period_inbase:
            period_inbase.remove(None)
    if len(period_inbase) < timelag:
         timelag=len(period_inbase)

    period_inbase = period_inbase[-timelag:]

    request.session['period_mth_rus'] = months_names(period_inbase)

    return period_inbase


def Get_Sales_Top(request, db_tbl, period_inbase):

    list_products = request.session['products_for_execute']
    dict_fields_short_show = request.session['dict_fields_short_show']


    if None in list_products:
        list_products.remove(None)

    #now = int(dt.strftime(dt.now(), "%m"))

    if list_products:
        total_ = Get_Prod_Execute_join_vardata(request, db_tbl, list_products, period_inbase)
    else:
        all_ = vlist_to_list(db_tbl['vardata'].objects.values_list('fk_products').distinct())
        total_ = Get_Prod_Execute_join_vardata(request, db_tbl, all_, period_inbase)

    if total_:
        df = read_frame(total_.order_by("-sales_sum"))
        fix_fields = {'id', 'brand', 'name', 'price_avg', 'appear_month'}
        for i in df.columns:
            if i not in fix_fields:
                if i not in set(dict_fields_short_show.keys()):
                    df.drop(i, axis='columns', inplace=True)
        rename_ttx = {k: v for k, v in dict_fields_short_show.items() if k not in fix_fields}
        df.rename(rename_ttx, axis='columns', inplace=True)

        exit_ = df

    else:
        exit_ = read_frame(db_tbl['vardata'].objects.none())

    return exit_

def Get_Shops(request, db_tbl, product_):

    product_in_shops = db_tbl['shop_prices'].objects.\
            filter(fk_products_shop=product_).order_by('modification_price')

    return product_in_shops

def Get_Bestsellers_links():

    qry = TextLinks.objects.all().order_by('-date')[:10]

    return qry

def about(request):

    try:
        categories_list = request.session['categories_list']
    except KeyError:
        ctg = Init_cat(request, '', {})
        categories_list = request.session['categories_list']

    exit_ = {'categories_list': categories_list}

    return render(request, template_name="al_about.html", context=exit_)


