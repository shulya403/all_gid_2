from django.shortcuts import render, HttpResponseRedirect
#from django.template import RequestContext
#from django.views.generic import View, DetailView, TemplateView
#from django.http import HttpResponse
from . import mkbl_urls

from django.conf import settings

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
    NbShopsPrices, \
    UpsClasses, \
    UpsProducts, \
    UpsProductsHasUpsClasses, \
    UpsVardata, \
    UpsShopsPrices, \
    TextLinks, \
    TxtHow, \
    TxtRatings


from datetime import datetime as dt
#import time
#import django_pandas as pd
import pandas as pdd
from django_pandas.io import read_frame
from django.db.models import Count, F, Sum, Avg, Q, Max

from django.template.defaulttags import register
from django.template.defaultfilters import linebreaksbr

import json
import os
import re
import django.core.exceptions

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
        except Exception:
            return 'n/a'
        exit_ = str()
        tail = len(str_digit) % 3
        for i in range(len(str_digit)-3, -1, -3):
            exit_ = "\xa0" + str_digit[i:i+3] + exit_

        if tail != 0:
            exit_ = str_digit[:tail] + exit_
            return exit_
        else:
            return exit_[1:]
    else:
        return 'n/a'

@register.filter
def digit_to_float(digit):
    if digit:
        try:
            str_digit = float(digit)
        except Exception:
            return 'n/a'

    else:
        return 'n/a'
    return str(str_digit)

@register.filter
def sort_keys(keys):

    return sorted(list(keys))

def DB_table(cat_):

    ORM_Models_names = {
    'Monitor': {
            'products': MntProducts,
            'classes': MntClasses,
            'mtm_prod_clas': MntProductsHasMntClasses,
            'vardata': MntVardata,
            'shop_prices': MntShopsPrices
            },

    'Noutbuk': { 'products': NbProducts,
            'classes': NbClasses,
            'mtm_prod_clas': NbProductsHasNbClasses,
            'vardata': NbVardata,
            'shop_prices': NbShopsPrices
        },

    'Printer-mfu': {'products': MfpProducts,
            'classes': MfpClasses,
            'mtm_prod_clas': MfpProductsHasMfpClasses,
            'vardata': MfpVardata,
            'shop_prices': MfpShopsPrices
        },
    'Ups': {'products': UpsProducts,
            'classes': UpsClasses,
            'mtm_prod_clas': UpsProductsHasUpsClasses,
            'vardata': UpsVardata,
            'shop_prices': UpsShopsPrices

    }

    }

    try:
        exit_ = ORM_Models_names[cat_]
    except KeyError:
        exit_ = None

    return exit_

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

def Get_static_dict(cat_):
    Static_dirs = {
        "Monitor": "Mnt",
        "Noutbuk": "Nb",
        "Printer-mfu": "Mfp"
    }
    if cat_ in Static_dirs.keys():
        return Static_dirs[cat_]
    else:
        return cat_

#Опредление категории
def Init_cat(request, cat_, db_tbl):


#Категории
    with open('marketability/static/marketability/json/dict_categories_new.json', encoding='utf-8') as f_cat:
        dict_categories = json.load(f_cat)

    if cat_:

        # Картинки для категории
        with open('marketability/static/marketability/json/dict_to_pic_new.json', encoding='utf-8') as f_pic:
            dict_to_cat = json.load(f_pic)[cat_]

        request.session['cat_'] = cat_

        request.session['static_dir'] = Get_static_dict(cat_)

        if dict_categories[cat_]["category_name_singular"]["stable"]:
            request.session['cat_singular'] = dict_categories[cat_]['category_name_singular']['name']
        else:
            request.session['cat_singular'] = ""
            request.session['cat_singular_fld'] = dict_categories[cat_]['category_name_singular']["field"]

        request.session['dict_to_cat'] = dict_to_cat

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

        request.session['period_inbase'] = Get_Period_inbase(request, db_tbl)

       # request.session['period_mth_rus'] = months_names(request.session['period_inbase'])

        request.session['form_return'] = []

        request.session['theme_pic'] = ('', None)

    else:
        request.session['categories_list'] = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]
        print(request.session['categories_list'])

        request.session['categories_list_singular'] = dict()
        for cat in dict_categories:
            request.session['categories_list_singular'][cat] = dict_categories[cat]['category_name_singular']['name']

        print(request.session['categories_list_singular'])

        request.session['cat_'] = cat_

        category = []

        request.session['theme_pic'] = ('', None)

    return category

# Формирование вложенного словаря по таблице _classes
def Dict_by_Classes2(request, db_tbl):

    # Картинки для категории
    with open('marketability/static/marketability/json/dict_sorting_classes_new.json', encoding='utf-8') as f_cls:
        dict_sorting_classes = json.load(f_cls)

    def Sort_dict_by_values(dict_):


        list_tuples = list(dict_.items())
        list_tuples.sort(key=lambda i: i[1])

        if list_tuples:
            exit_ = [i[0] for i in list_tuples]
        else:
            exit_ = []


        return exit_

    def Sort_Sub_types(Sub_types_list, cat_, level='sub_types'):

        exit_ = list()
        sorted_list_ = Sort_dict_by_values(dict_sorting_classes[cat_][level])
        if sorted_list_:
            for sbt in Sub_types_list:
                if not sbt in sorted_list_:
                        exit_.append(sbt)
            for sbt in sorted_list_:
                if sbt in Sub_types_list:
                    exit_.append(sbt)
        else:
            exit_ = Sub_types_list

        return exit_

    def Sort_Classes_in_sbtype(qry_classes, cat_, level='classes'):

        exit_ = list()
        sorted_list_ = Sort_dict_by_values(dict_sorting_classes[cat_][level])

        if sorted_list_:

            for cls in qry_classes:
                if not cls['text'] in sorted_list_:
                    exit_.append(cls)
            for txt in sorted_list_:
                for i in qry_classes:
                    if i['text'] == txt:
                        exit_.append(i)
                        break
        else:
            exit_ = list(qry_classes)

        return exit_

    def Dict_class_subtype(cl_type, qry_classes, cat_):

        exit_sub_ = dict()
        qry_subtype = qry_classes.filter(type=cl_type)
        list_sub_types_ = vlist_to_list(qry_subtype.values_list('class_subtype').distinct())

        list_sub_types_sorted = Sort_Sub_types(list_sub_types_, cat_)

        for sub_type in list_sub_types_sorted:
            if not sub_type:
                st_name = '1'
            else:
                st_name = sub_type
            exit_sub_[st_name] = list()
            cls_ = qry_subtype.filter(class_subtype=sub_type).values('name', 'explanation', 'text')
            cls = Sort_Classes_in_sbtype(cls_, cat_)
            for i in cls:
                exit_sub_[st_name].append(i)

        return exit_sub_

    exit_ = dict()
    qry_classes = db_tbl['classes'].objects.all()

    request.session['list_enabled'] = vlist_to_list(qry_classes.values_list('name'))
    print(request.session['list_enabled'])

    for cl_type in vlist_to_list(qry_classes.values_list('type').distinct()):
        exit_[cl_type] = Dict_class_subtype(cl_type, qry_classes, request.session['cat_'])

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
        .values('fk_products', 'fk_classes')


# .order_by('fk_products') \

    return products_mtm


def Cat_Check_for_Redirect(cat_):
    dict_old_cat_names = {
        'Nb': 'Noutbuk',
        'Mnt': 'Monitor',
        'Mfp': 'Printer-mfu'
    }

    if cat_ in dict_old_cat_names.keys():
        str_redirect = dict_old_cat_names[cat_]
        return str_redirect

    else:
        return cat_

def page_Category_Main(request, cat_):

    #Обновление параметров категории - даннае для формы и прочее

    cat_check = Cat_Check_for_Redirect(cat_)
    if cat_check != cat_:
        return HttpResponseRedirect("/" + cat_check + '/')

    db_tbl = DB_table(cat_)

    if db_tbl:
        try:
            if cat_ != request.session['cat_']:
                category = Init_cat(request, cat_, db_tbl)

        except KeyError:
            category = Init_cat(request, cat_, db_tbl)

        new_form = request.session['new_form']
        list_enabled = request.session['list_enabled']
        category_name = request.session['cat_rus_name']
        categories_list = request.session['categories_list']
        tab_active = request.session['tab_active']
        tab_data = Dict_tabs_page_form()
        tab_list = list(tab_data.keys())
        str_period_inbase = request.session['period_inbase']
        period_inbase = Recover_Date_period_inbase(str_period_inbase)
        period = request.session['period_mth_rus']
        theme_pic = request.session['theme_pic']


        if request.GET:
            #print(request.GET)
            post_return = list(request.GET.keys())
            tab_active = request.GET['tabs']
            if 'csrfmiddlewaretoken' in post_return:
              post_return.remove('csrfmiddlewaretoken')

            post_return.remove('tabs')

            if 'goals_fbb_mobile' in post_return:
                goals_fbb_mobile = True
                post_return.remove('goals_fbb_mobile')
            else:
                goals_fbb_mobile = False

            if 'classes_fbb_mobile' in post_return:
                classes_fbb_mobile = True
                post_return.remove('classes_fbb_mobile')
            else:
                classes_fbb_mobile = False

            request.session['form_return'] = post_return

            products_mtm = Get_Products_Mtm(post_return, db_tbl)

            # products_for_execute - list id отфильторванных моделей
            products_for_execute = vlist_to_list(list(products_mtm.values_list('fk_products').distinct()))

            request.session['products_for_execute'] = products_for_execute

            # classes_for_execute - list id доступных после фильтра классов
            classes_for_execute = vlist_to_list(list(products_mtm.values_list('fk_classes').distinct()))
            print(classes_for_execute )

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

            goals_fbb_mobile = False
            classes_fbb_mobile = False

            #products_for_execute = request.session['products_for_execute']

        df_data = Get_Sales_Top(request, db_tbl, period_inbase)

        if not df_data.empty:
            request.session['dict_df_data'] = df_data[['id', 'id_brand_name', 'brand', 'name', 'price_avg']].to_dict()
        else:
            request.session['dict_df_data'] = {}

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

        #best_links = Get_Bestsellers_links()
        best_links = Get_Ratings_links(cat_)

        if (not theme_pic[1]) \
            or (not theme_pic[0] in post_return):
                theme_pic = Choice_Pic(request.session['dict_to_cat'], post_return, method='first_choice')
                request.session['theme_pic'] = theme_pic

        theme_pic_this = theme_pic[1]

        exit_ = {
            'category_name':  category_name,
            'categories_list': categories_list,
            'action': cat_,
            'tbl_ttx_col': [x for x in tab_marketability.keys() if x not in ['id', 'id_brand_name', 'brand', 'name', 'price_avg', 'appear_month']],
            'tbl_data': tab_marketability,
            'tbl_data_nov': tab_novelty,
            'new_form': new_form,
            'enabled': enabled_return,
            'checked_items': post_return,
            'period': period,
            'bestesellers_links': best_links[0],
            'bestesellers_cat': best_links[1],
            'tab_active': tab_active,
            'tab_list': tab_list,
            'tab_data': tab_data,
            'theme_pic': theme_pic_this,
            'goals_fbb_mobile': goals_fbb_mobile,
            'classes_fbb_mobile': classes_fbb_mobile
        }


        return render(request, template_name="category_get_url.html", context=exit_)
    else:
        return handler404(request)

def Product_Check_for_Redirect(product_, tbl_products):

    if re.match(r'\d+$', str(product_)):
        try:
            row_product = tbl_products.objects.get(id=product_)
            return row_product.id_brand_name
        except Exception:
            return None

    else:
        return product_


def page_new_Product(request, cat_, product_):
    def df_Cat_Init_(request, cat_init):
        if cat_init:
            category = Init_cat(request, cat_, db_tbl)
            request.session['enabled_return'] = request.session['list_enabled']
            request.session['products_for_execute'] = []
        else:
            products_for_execute_keep = request.session['products_for_execute']
            enabled_return_keep = request.session['enabled_return']
            request.session['enabled_return'] = request.session['list_enabled']
            request.session['products_for_execute'] = []

        str_period_inbase = request.session['period_inbase']
        period_inbase = Recover_Date_period_inbase(str_period_inbase)
        df_data = Get_Sales_Top(request, db_tbl, period_inbase)

        if cat_init:
            if not df_data.empty:
                request.session['dict_df_data'] = df_data[['id', 'brand', 'name', 'price_avg']].to_dict()
            else:
                request.session['dict_df_data'] = {}
        else:
            request.session['products_for_execute'] = products_for_execute_keep
            request.session['enabled_return'] = enabled_return_keep

        return (df_data, period_inbase)

    cat_check = Cat_Check_for_Redirect(cat_)

    db_tbl = DB_table(cat_check)
    #print(cat_check)
    product_chek = Product_Check_for_Redirect(product_, db_tbl['products'])
    #print(product_chek)

    if not product_chek:
        return handler404(request)

    if (cat_check != cat_) or (product_chek != product_):

        return HttpResponseRedirect("/" + cat_check + "/" + product_chek)


    if db_tbl:
        try:
            if not request.session['cat_'] == cat_check:
                cat_init = True
            else:
                cat_init = False
        except KeyError:
            cat_init = True
        finally:
            df_data, period_inbase = df_Cat_Init_(request, cat_init)
            # df_data =  df_Cat_Init_(request, cat_init)[0]
            # period_inbase =

        new_form = request.session['new_form']
        form_return = request.session['form_return']
        category_name = request.session['cat_rus_name']


        categories_list = request.session['categories_list']

        try:
            Product = db_tbl['products'].objects.get(id_brand_name=product_chek)
        except django.core.exceptions.MultipleObjectsReturned:
            Product = db_tbl['products'].objects.filter(id_brand_name=product_chek).values()

            try:
                true_id = df_data[df_data['id_brand_name'] == product_chek]['id'].values[0]
            except Exception:
                true_id = None
            #print(true_id)
            if true_id:
                Product = db_tbl['products'].objects.get(id=true_id)
            else:
                id_max = Product.aggregate(Max('id'))
                Product = db_tbl['products'].objects.get(id=id_max['id__max'])

        if Product:

            if request.session['cat_singular']:
                category_name_singilar = request.session['cat_singular']
            else:
                try:
                    category_name_singilar = Product[request.session['cat_singular_fld']]
                except Exception:
                    category_name_singilar = category_name

            fields_ = [f.name for f in db_tbl['products']._meta.get_fields()]

            list_this_classes = Get_This_Classes(Product.id, db_tbl)
            this_classes = db_tbl['classes'].objects.filter(id__in=list_this_classes)

            miscell_products, df_miscell = Get_Miscell_Products(Product.id, set(vlist_to_list(list_this_classes)), df_data, db_tbl)

            dict_ttx = dict()
            set_fields_show = set(request.session['dict_sorted_fields_show'].keys()) - {'brand', 'name'}
            set_fields_not_show = set(fields_) - set_fields_show
            #dict_html_names = Fld_html_names(request, fields_, ['brand', 'name', 'id'])
            dict_html_names = Fld_html_names(request, fields_, set_fields_not_show)

            for i in request.session['dict_sorted_fields_show'].keys():
                if i not in set_fields_not_show:
                    dict_ttx[dict_html_names[i]] = Product.__getattribute__(i)


            shop_mod = Get_Shops(request, db_tbl, Product.id)

            #price
            this_price = df_data[df_data['name'] == Product.name]['price_avg'].values

            #Картинка
            prod_img_list = Get_Prod_Images(Make_Prod_Image_name(Product), request.session['static_dir'])
            if prod_img_list:
                prod_img_one = "/static/marketability/pict/" + request.session['static_dir'] + "/" + prod_img_list[0]
            else:
                prod_img_one = ""

            best_links = Get_Ratings_links(request.session['static_dir'])

            if this_price:
                price_min_short, price_max_short, this_price_short, price_rate = Get_Price_Rate(df_miscell, this_price[0])

                miscell_sorted_list = df_miscell['id_brand_name'].to_list()
                min_product = miscell_sorted_list[0]
                max_product = miscell_sorted_list[-1]

                if Product.id_brand_name != min_product:
                    last_product = df_miscell.iloc[miscell_sorted_list.index(Product.id_brand_name) - 1]['id_brand_name']
                else:
                    last_product = Product.id_brand_name
                if Product.id_brand_name != max_product:
                    next_product = df_miscell.iloc[miscell_sorted_list.index(Product.id_brand_name) + 1]['id_brand_name']

                else:
                    next_product = Product.id_brand_name

            else:
                price_rate = "no"
                price_min_short = ""
                price_max_short = ""
                this_price_short = ""
                min_product = ""
                max_product  = ""
                last_product = ""
                next_product = ""

            exit_ = {
                'category_name': category_name,
                'category_name_singular': category_name_singilar,
                'categories_list': categories_list,
                'vendor': Product.brand,
                'name': Product.name,
                'ttx': dict_ttx,
                'new_form': new_form,
                'checked_items': form_return,
                'shop_mod': shop_mod,
                'action': cat_,
                'this_price': this_price,
                'miscell': miscell_products,
                'len_miscell': len(df_miscell),
                'this_classes': this_classes,
                'id': Product.id,
                'id_brand_name': Product.id_brand_name,
                'prod_img': prod_img_one,
                'bestesellers_links': best_links[0],
                'bestesellers_cat': best_links[1],
                'price_rate': price_rate,
                'price_min_short': price_min_short,
                'price_max_short': price_max_short,
                'len_price_max_short': len(price_max_short) * 8,
                'this_price_short': this_price_short,
                'min_product': min_product,
                'max_product': max_product,
                'last_product': last_product,
                'next_product': next_product

            }

            return render(request, template_name="new_product_url.html", context=exit_)
        else:
            return handler404(request)
    else:
        return handler404(request)

def Get_Price_Rate(df_miscell, this_price):


    max_price = df_miscell['price_avg'].max()
    min_price = df_miscell['price_avg'].min()

    try:
        price_rate = round((this_price - min_price) / (max_price - min_price), 2) * 100
    except ZeroDivisionError:
        price_rate = None

    max_price_short = str(round(max_price / 1000, 1))
    min_price_short = str(round(min_price / 1000, 1))
    this_price_short = str(round(this_price / 1000, 1))

    return (min_price_short, max_price_short, this_price_short, price_rate)

#Подбор картинки
def Choice_Pic(dict_to_pic, post_return, method='first_choice'):


    def First_choice(dict_to_pic, post_return):

        if dict_to_pic:

            for go in dict_to_pic:
                if go in post_return:
                    return (go, dict_to_pic[go])
            return ('zaglushka', dict_to_pic['zaglushka'])
        else:
            return ('zaglushka', 'pict/themes/cabinet-home-clown.jpg')


    if method == 'first_choice':
        exit_ = First_choice(dict_to_pic, post_return)


    return exit_



#Список классов конкретного продукта
def Get_This_Classes(product_, db_tbl):

    return db_tbl['mtm_prod_clas'].objects.filter(fk_products=product_).values_list('fk_classes')

#Список продуктов с идентичным набором классов что и у данного продукта
def Get_Miscell_Products(product_, set_this_classes, df_data, db_tbl):

    list_df_data = df_data['id'].to_list()


    qry_miscell = db_tbl['mtm_prod_clas'].objects.filter(fk_products__in=list_df_data).\
        values('fk_products').distinct().annotate(fcl = F('fk_classes'))
    #print(qry_miscell)
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

    df_miscell = df_data[df_data['id'].isin(products_miscell)].sort_values(by=['price_avg'])

    df_miscell_vendor = df_miscell[['brand', 'id', 'id_brand_name', 'name', 'price_avg']].groupby('brand')
    agg_miscell_vendor = df_miscell_vendor[['id', 'name', 'id_brand_name', 'price_avg']].agg(list)

    dict_miscell_vendor = dict()
    for i, row in agg_miscell_vendor.iterrows():
        list_name_price = list()

        q = len(row['name'])
        for j in range(q):
            list_name_price.append({'id': row['id'][j], 'id_brand_name': row['id_brand_name'][j], 'name': row['name'][j], 'price': row['price_avg'][j]})

        dict_miscell_vendor[i] = list_name_price

    return dict_miscell_vendor, df_miscell

def Make_Prod_Image_name(qry_product):
    exit_ = qry_product.brand.lower() + "_" + qry_product.name.lower().replace(" ", "_").replace("/", ", ").replace(".", "_")

    if exit_:
        return exit_
    else:
        return ""

def Get_Prod_Images(prod_image_name, cat):

    directory_ = settings.BASE_DIR + "/marketability/static/marketability/pict/" + cat

    try:
        return [file_img for file_img in os.listdir(directory_) if prod_image_name in file_img]
    except Exception:
        return []

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

    #sales_sum = cat_def.lower() + "vardata__sales_units"
    db_vardata_string = db_tbl['vardata']._meta.model_name

    sales_sum = db_vardata_string  + "__sales_units"
    filter_months = {
        #cat_def.lower() + "vardata__month__in": qry_period
        db_vardata_string + "__month__in": qry_period
    }
    #price_avg = cat_def.lower() + "vardata__price_rur"
    price_avg = db_vardata_string + "__price_rur"
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

    if len(period_) > 1:
        date_tuple = (period_[0], period_[-1])
        if date_tuple[0].year > date_tuple[1].year:
            date_tuple = (date_tuple[1], date_tuple[0])

        if date_tuple[0].year == date_tuple[1].year:
            exit_ = mth_names[date_tuple[0].month] + \
                    "\u2013" + \
                    mth_names[date_tuple[1].month] + \
                    " " + str(date_tuple[0].year)
        else:
            exit_ = mth_names[date_tuple[0].month] + \
                    "`" + date_tuple[0].strftime("%y") + \
                    "\u2013" + \
                    mth_names[date_tuple[1].month] + \
                    "`" + date_tuple[1].strftime("%y")
    else:
        try:
            exit_ = mth_names[period_[0].month] + "`" + period_[0].strftime("%y")
        except:
            exit_ = "2021"

    return exit_

def Get_Period_inbase(request, db_tbl):

    timelag = request.session['timelag']

    period_inbase = vlist_to_list(db_tbl['vardata'].objects.values_list('month').distinct().order_by('month'))

    if None in period_inbase:
            period_inbase.remove(None)
    if len(period_inbase) < timelag:
         timelag=len(period_inbase)

    period_inbase = period_inbase[-timelag:]


    request.session['period_mth_rus'] = months_names(period_inbase)

    exit_str = [date_.strftime('%Y.%m.%d') for date_ in period_inbase]


    return exit_str

def Recover_Date_period_inbase(str_period_inbase):

    exit_ = [dt.strptime(str_, '%Y.%m.%d').date() for str_ in str_period_inbase]

    return exit_


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
        fix_fields = {'id', 'brand', 'name', 'id_brand_name', 'price_avg', 'appear_month'}
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

    # try:
    #     categories_list = request.session['categories_list']
    # except KeyError:
    ctg = Init_cat(request, '', {})
    categories_list = request.session['categories_list']

    exit_ = {'categories_list': categories_list}

    return render(request, template_name="al_about.html", context=exit_)

def home(request):
    # try:
    #     categories_list = request.session['categories_list']
    #except KeyError:
    ctg = Init_cat(request, '', {})
    categories_list = request.session['categories_list']

    categories_pict = {
        "Ноутбуки": "/static/marketability/pict/cat/nb.jpg",
        "Мониторы": "/static/marketability/pict/cat/Mnt.jpg",
        "Принтеры и МФУ": "/static/marketability/pict/cat/Mfp.jpg",
        "ИБП": "/static/marketability/pict/cat/Ups.jpg"
    }

    exit_ = {'categories_list': categories_list,
             'categories_pict': categories_pict}

    return render(request, template_name="al_home.html", context=exit_)

def search_all(request):
    # try:
    #     categories_list = request.session['categories_list']
    # except KeyError:
    ctg = Init_cat(request, '', {})
    categories_list = request.session['categories_list']
    dict_cat_model_list = dict()
    for cat_ in categories_list:
        db_tbl = DB_table(cat_[1])
        qry_all = db_tbl['products'].objects.all().order_by('brand', 'name').values('id', 'brand','name', 'id_brand_name')
        dict_cat_model_list[cat_[1]] = qry_all


    exit_ = {'categories_list': categories_list,
             'dict_cat': dict_cat_model_list
             }

    return render(request, template_name="search_all.html", context=exit_)

def handler404(request, exception=None):

    # try:
    #     categories_list = request.session['categories_list']
    # except KeyError:
    ctg = Init_cat(request, '', {})
    categories_list = request.session['categories_list']

    response = render(request, template_name="404.html", context={'categories_list': categories_list})
    response.status_code = 404

    return response
def Get_Ratings_links(cat_):

    dict_cat = {
        "Monitor": "Mnt",
        "Noutbuk": "Nb",
        "Printer_mfu": "Mfp"
    }

    if cat_ in dict_cat.keys():
        cat_ = dict_cat[cat_]

    listing = TxtRatings.objects.filter(cat=cat_).values('idtxt_ratings', 'cat', 'id_html_name', 'article_title', 'article_anno', 'img', 'pin',
                                                         'date').order_by('-date')
    len_list = len(listing)
    if len_list > 5:
        return (listing[:5], cat_)
    else:
        return (listing, cat_)

