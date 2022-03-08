# TODO:
## Возврат из Product tab
## Пикты табов Топ и ВСЕ
## Ноутбуки все - число
## Новый дийзайн мобилы формы
## Зкщвгсе Page Shifting Loyaut
## Звезды механизм
## Звезды БД
## Звезды Вывод
## Core Vitals Ыршаештп
## возврат на открытый tab_active



# пересечение enabled classes и вендорс
# Ширина блока формы в дектопе
# Заголовки блоков формы
# вверху кнопки
## Кнопки очистить все
## Возврат в нужную форму

from django.shortcuts import render, HttpResponseRedirect
#from django.template import RequestContext
#from django.views.generic import View, DetailView, TemplateView
#from django.http import HttpResponse
#from . import mkbl_urls
import django_user_agents
from django_user_agents.utils import get_user_agent

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

@register.filter
def replace_space(symbol, string):
    return string.replace(" ", symbol)

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
        'top5': {
            "rus_name": "Топ 5",
            "img_active": "top-gist-active.svg",
            "img_noactive": "top-gist-noactive.svg",
            "Q": 5,
            "img_symbol": "&#10031;",
            "img_active_color": ""
        },
        'top10': {
            "rus_name": "Топ 10",
            "img_active": "top-gist-active_top10.svg",
            "img_noactive": "top-gist-noactive_top10.svg",
            "Q": 10,
            "img_symbol": "&#10031;",
            "img_active_color": ""
        },
        'top20': {
            "rus_name": "Топ 20",
            "img_active": "top-gist-active_top20.svg",
            "img_noactive": "top-gist-noactive_top20.svg",
            "Q": 20,
            "img_symbol": "&#10031;",
            "img_active_color": ""
        },
        'all': {
            "rus_name": "ВСЕ",
            "img_active": "Tital_expand grey_active.svg",
            "img_noactive": "Tital_expand grey_noactive.svg",
            "img_symbol": "&#10031;",
            "img_active_color": ""
        },
        'novelity': {
            "rus_name": "НОВИНКИ",
            "img_active": "Gray white.svg",
            "img_noactive": "Lamp gray-1.svg",
            "img_symbol": "&#10031;",
            "img_active_color": ""
        }

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

        request.session['vendors'] = vlist_to_list(db_tbl['products'].objects.all().values_list('brand').distinct())
        #print(request.session['vendors'])

        request.session['new_form'] = Dict_by_Classes2(request, db_tbl)

        request.session['enabled_return'] = request.session['list_enabled']

        request.session['tab_active'] = 'top5'

        request.session['timelag'] = category['timelag']

        request.session['period_inbase'] = Get_Period_inbase(request, db_tbl)

        filter_brands_month = {
            db_tbl['vardata']._meta.model_name + "__month__in": Recover_Date_period_inbase(request.session['period_inbase'])}

        request.session['vendors_enabled'] = vlist_to_list(db_tbl['products'].objects.filter(**filter_brands_month).values_list('brand').distinct())

       # request.session['period_mth_rus'] = months_names(request.session['period_inbase'])

        request.session['form_return'] = []

        request.session['vendors_checked'] = []

        request.session['theme_pic'] = ('', None)

    else:
        request.session['categories_list'] = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]
        #print(request.session['categories_list'])

        request.session['categories_list_singular'] = dict()
        for cat in dict_categories:
            request.session['categories_list_singular'][cat] = dict_categories[cat]['category_name_singular']['name']

        #print(request.session['categories_list_singular'])

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
    #print(request.session['list_enabled'])

    for cl_type in vlist_to_list(qry_classes.values_list('type').distinct()):
        exit_[cl_type] = Dict_class_subtype(cl_type, qry_classes, request.session['cat_'])

    return exit_

def vlist_to_list(vlist):
    return [i[0] for i in vlist]

# Получение выборки из mtm только с продуктами встр. в отфильтрованных формой классах вендорах
def Get_Products_Mtm(request, post_return, vendors_checked, db_tbl, period_inbase):

    if post_return:
        post_return_ = post_return
    else:
        post_return_ = request.session['list_enabled']

    if vendors_checked:
        vendors_checked_ = vendors_checked
    else:
        vendors_checked_ = request.session['vendors_enabled']

    # joined_mtm - выборка из mtm по отфильтрованным классам и вендорам
    period_models = vlist_to_list(db_tbl['vardata'].objects.filter(month__in=period_inbase).values_list('fk_products'))

    print("post_return_mtm", post_return_)
    print("vendors_checked__mtm", vendors_checked)

    joined_mtm = db_tbl['mtm_prod_clas'].objects \
        .filter(fk_classes__name__in=post_return_, fk_products__brand__in = vendors_checked_) \
        .values('fk_products', 'fk_classes') \
        .filter(fk_products__in=period_models)


    # inner_join_products число упоминаний продуктов в отфильтрованной таблице mtm
    inner_join_products = joined_mtm.values('fk_products') \
        .annotate(Count('fk_products'))

    # inner_join_products_ - только продукты из inner_join встр в количестве классов равном числу отдачи формы
    if post_return:
        inner_join_products_ = inner_join_products \
            .filter(fk_products__count=len(post_return)) \
            .values_list('fk_products')
    else:
        inner_join_products_ = inner_join_products.values_list('fk_products')

    # products_mtm - список записей в mtm с продуктом присутсв. во всех отфильтрованных классах
    products_mtm = db_tbl['mtm_prod_clas'].objects \
        .filter(fk_products__in=inner_join_products_) \
        .values('fk_products', 'fk_classes')

    print(products_mtm)

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
        vendors_enabled = request.session['vendors_enabled']
        category_name = request.session['cat_rus_name']
        categories_list = request.session['categories_list']
        tab_active = request.session['tab_active']
        tab_data = Dict_tabs_page_form()
        try:
            tab_active_data = tab_data[tab_active]
        except KeyError:
            tab_active = "top5"
            tab_active_data = tab_data[tab_active]
            request.session['tab_active'] = tab_active

        tab_list = list(tab_data.keys())

        list_vendors_all = request.session['vendors']

        str_period_inbase = request.session['period_inbase']
        period_inbase = Recover_Date_period_inbase(str_period_inbase)
        period = request.session['period_mth_rus']
        theme_pic = request.session['theme_pic']


            #if request.GET:
        post_return = list(request.GET.keys())
        print("request.GET -> ", request.GET)
        try:
            page_place = request.GET['infocus-now']
        except KeyError:
            page_place = "up"

        try:
            tab_active = request.GET['tabs']
            tab_active_data = tab_data[tab_active]
            post_return.remove ('tabs')
            print(tab_active_data)
        except KeyError:
            tab_active = "top5"
            tab_active_data = tab_data[tab_active]
            try:
                post_return.remove('tabs')
            except:
                pass

            print(tab_active_data)
        finally:
            request.session['tab_active'] = tab_active

        if 'csrfmiddlewaretoken' in post_return:
            post_return.remove ('csrfmiddlewaretoken')

        if 'infocus-now' in post_return:
            post_return.remove('infocus-now')


        vendors_checked, post_return = Get_vendors_checked(post_return)

        request.session['vendors_checked'] = vendors_checked
        request.session['form_return'] = post_return
        print ('vendors_checked -> ', vendors_checked)
        print ('post_return -> ', post_return)

        products_mtm = Get_Products_Mtm (request, post_return, vendors_checked, db_tbl, period_inbase)

        # products_for_execute - list id отфильторванных моделей
        products_for_execute = vlist_to_list (list (products_mtm.values_list ('fk_products').distinct ()))
        request.session['products_for_execute'] = products_for_execute

        # classes_for_execute - list id доступных после фильтра классов
        classes_for_execute = vlist_to_list (list (products_mtm.values_list ('fk_classes').distinct ()))

        # print(products_for_execute)
        list_enabled_ = db_tbl['classes'].objects.filter (id__in=classes_for_execute).values_list ('name')
        list_enabled_ = vlist_to_list (list (list_enabled_))
        # print(list_enabled_)
        if list_enabled_:
            request.session['enabled_return'] = list_enabled_
        else:
            request.session['enabled_return'] = list_enabled

        enabled_return = request.session['enabled_return']

        if post_return:
            id_post_chek = db_tbl['classes'].objects.filter (name__in=post_return).values_list ('id')
            print(post_return)
            qry_vendors_enabled = {
                db_tbl['vardata']._meta.model_name + "__month__in": period_inbase,
                db_tbl['mtm_prod_clas']._meta.model_name + "__fk_classes__in": id_post_chek
            }
        else:
            qry_vendors_enabled = {
                db_tbl['vardata']._meta.model_name + "__month__in": period_inbase
            }

            # qry_vendors_enabled = {
            #     db_tbl['vardata']._meta.model_name + "__month__in": period_inbase,
            #     "id__in": products_for_execute
            # }

            vendors_enabled_ = db_tbl['products'].objects.\
                filter(**qry_vendors_enabled).distinct().\
                values_list('brand')
            vendors_enabled_ = vlist_to_list(list(vendors_enabled_))

            print('vendors_enabled', vendors_enabled_)

            if vendors_enabled_:
                request.session['vendors_enabled'] = vendors_enabled_
            else:
                request.session['vendors_enabled'] = vendors_enabled

            vendors_enabled = request.session['vendors_enabled']

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

        # else:
        #     tab_active = "top5"
        #     tab_active_data = tab_data[tab_active]
        #     post_return = request.session['form_return']
        #     vendors_checked = request.session['vendors_checked']
        #     enabled_return = request.session['enabled_return']
        #     vendors_enabled = request.session['vendors_enabled']


            # if post_return:
            #     pass
            # else:
            #     #request.session['products_for_execute'] = []

        goals_fbb_mobile = False
        classes_fbb_mobile = False

            #products_for_execute = request.session['products_for_execute']

        df_data = Get_Sales_Top(request, db_tbl, period_inbase)

        if not df_data.empty:
            if vendors_checked:
                df_data = df_data[df_data['brand'].isin(vendors_checked)]
            #request.session['dict_df_data'] = df_data[['id', 'id_brand_name', 'brand', 'name', 'price_avg']].to_dict()

        #else:
            #request.session['dict_df_data'] = {}

        q_data = len(df_data)

        if q_data > 0:

            if "Q" in tab_active_data.keys():
                q_tab = tab_data[tab_active]["Q"]
            else:
                q_tab = q_data
            if tab_active == "novelity":
                tbl_data = df_data[df_data['appear_month'].isin(period_inbase)].sort_values('price_avg').to_dict()
            else:
                tbl_data = df_data[:q_tab].sort_values('price_avg').to_dict()

        else:
            tbl_data = dict()
            # tab_novelty = dict()


        # best_links = Get_Bestsellers_links()
        best_links = Get_Ratings_links(cat_)

        if (not theme_pic[1]) \
                or (not theme_pic[0] in post_return):
            theme_pic = Choice_Pic(request.session['dict_to_cat'], post_return, method='first_choice')
            request.session['theme_pic'] = theme_pic

        theme_pic_this = theme_pic[1]

        exit_ = {
            'category_name': category_name,
            'categories_list': categories_list,
            'action': cat_,
            'tbl_ttx_col': [x for x in tbl_data.keys() if
                            x not in ['id', 'id_brand_name', 'brand', 'name', 'price_avg', 'appear_month']],
            'tbl_data': tbl_data,
            # 'tbl_data_nov': tab_novelty,
            'new_form': new_form,
            'enabled': enabled_return,
            'checked_items': post_return,
            'period': period,
            'bestesellers_links': best_links[0],
            'bestesellers_cat': best_links[1],
            'tab_active': tab_active,
            'tab_list': tab_list,
            'tab_data': tab_data,
            'tab_active_data': tab_active_data,
            'theme_pic': theme_pic_this,
            'goals_fbb_mobile': goals_fbb_mobile,
            'classes_fbb_mobile': classes_fbb_mobile,
            'vendors_all': list_vendors_all,
            'vendors_checked': vendors_checked,
            'vendors_enabled': vendors_enabled,
            'page_place': page_place
        }



        return UA_Category_Main_Render(request, exit_)
            #render(request, template_name="category_get_url.html", context=exit_)
    else:
        return handler404(request)

def Get_vendors_checked(post_return):

    print('GET -> ', post_return)
    exit_list = [ven.replace("ven__", "") for ven in post_return if "ven__" in ven]
    post_return_exit = [go_cl for go_cl in post_return if "ven__" not in go_cl]

    return exit_list, post_return_exit


def UA_Category_Main_Render(request_, exit_):
    try:
        user_agent = get_user_agent(request_)
        if user_agent.is_pc:
            # print("page+place -> ", exit_['page_place'])
            # if exit_['page_place'] == 'up':
            #     return render(request_, template_name="category_get_desktop_2.html", context=exit_)
            # elif exit_['page_place'] in ['GO', 'CL']:
            #     return render(request_, template_name="category_get_desktop_2.html#GO_CL", context=exit_)
            # elif exit_['page_place'] == 'ven':
            #     print("вендор")
            #     # return render(request_, template_name="category_get_desktop_2.html#VEN__", context=exit_)
            # else:
            return render(request_, template_name="category_get_desktop_2.html", context=exit_)
        elif user_agent.is_mobile:
            return render(request_, template_name="category_get_mobile_2.html", context=exit_)
        elif user_agent.is_tablet:
            return render(request_, template_name="category_get_desktop_2.html", context=exit_)

    except Exception:
        return render(request_, template_name="category_get_desktop_2.html", context=exit_)

    return render(request_, template_name="category_get_desktop_2.html", context=exit_)


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
            #request.session['enabled_return'] = request.session['list_enabled']
            #request.session['products_for_execute'] = []
        #else:
            #products_for_execute_keep = request.session['products_for_execute']
            #enabled_return_keep = request.session['enabled_return']
            #request.session['enabled_return'] = request.session['list_enabled']
            #request.session['products_for_execute'] = []

        str_period_inbase = request.session['period_inbase']
        period_inbase = Recover_Date_period_inbase(str_period_inbase)
        df_data = Get_Sales_Top_for_miscell(request, db_tbl, period_inbase)

        # if cat_init:
        #     if not df_data.empty:
        #         request.session['dict_df_data'] = df_data[['id', 'brand', 'name', 'price_avg']].to_dict()
        #     else:
        #         request.session['dict_df_data'] = {}
        # else:
        #     request.session['products_for_execute'] = products_for_execute_keep
        #     request.session['enabled_return'] = enabled_return_keep

        return (df_data, period_inbase)

    cat_check = Cat_Check_for_Redirect(cat_)

    db_tbl = DB_table(cat_check)
    if not db_tbl:
        return handler404(request)
    #print(cat_check)
    product_chek = Product_Check_for_Redirect(product_, db_tbl['products'])
    #print(product_chek)

## TODO: Передеать редирект из views_new
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
        #all_ = vlist_to_list(db_tbl['vardata'].objects.values_list('fk_products').distinct())
        total_ = [] #Get_Prod_Execute_join_vardata(request, db_tbl, all_, period_inbase)

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

def Get_Sales_Top_for_miscell(request, db_tbl, period_inbase):

    all_ = vlist_to_list(db_tbl['vardata'].objects.values_list('fk_products').distinct())
    return read_frame(Get_Prod_Execute_join_vardata(request, db_tbl, all_, period_inbase))[['id', 'brand', 'name', 'id_brand_name', 'price_avg', 'appear_month']]

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

