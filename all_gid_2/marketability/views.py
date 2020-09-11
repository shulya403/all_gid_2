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
    MfpVardata
from datetime import datetime as dt
from datetime import date


#from django import forms
from pprint import pprint
from django.db.models import Count, F, Sum

#class AllgidBase(TemplateView):

#    template_name = "test.html"
#    slug_url_kwarg = "cat_"
#    query_pk_and_slug = True
#    model = self.kwargs['cat_']




    # def dispatch(self, request, *args, **kwargs):
    #     exit_ = {
    #         "word": self.cat_ + self.
    #     }
    #     return render(request, template_name="test.html", context=exit_)




dict_categories = {
        'Mnt': {
            'category_name': "Мониторы",
            'db_tables':    {
                'products': MntProducts,
                'classes': MntClasses,
                'mtm_prod_clas': MntProductsHasMntClasses,
                'vardata': MntVardata
            }
        },
        'Nb': {
            'category_name': "Ноутбуки",
            'db_tables':    {
                'products': NbProducts,
                'classes': NbClasses,
                'mtm_prod_clas': NbProductsHasNbClasses,
                'vardata': NbVardata
            }
        },
        'Mfp': {
            'category_name': "Принтеры и МФУ",
            'db_tables': {
                'products': MfpProducts,
                'classes': MfpClasses,
                'mtm_prod_clas': MfpProductsHasMfpClasses,
                'vardata': MfpVardata
            }
        }
    }


#class Form_classes(forms.Form):


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
form_return = ""

def page_Category_Main(request, cat_):

    global form_return

    category = dict_categories[cat_]
    db_tbl = category['db_tables']

    categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    form_fld = db_tbl['classes'].objects.all()
    list_enabled = vlist_to_list(list(form_fld.values_list('name')))

    if request.POST:
        #pprint(request.POST)
        post_return = list(request.POST.keys())
        post_return.remove('csrfmiddlewaretoken')
        form_return = post_return
        print(post_return)

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
        list_products = db_tbl['products'].objects.filter(id__in=products_for_execute).values('name')
        #pprint(list_products)
    else:
        post_return = []
        enabled_return = list_enabled
        joined_mtm = "пусто"
        tbl_joined = {"1": 0, "2": 0}
        list_products = []

    tab_marketability = Get_Sales_Top(db_tbl, list_products, q=10)

    dict_form_fld = Dict_by_Classes(form_fld)
    Form_by_dict_classes(dict_form_fld, post_return, enabled_return)

    exit_ = {
        'category_name':  category['category_name'],
        'categories_list': categories_list,
        'action': cat_,
#        'form': html_form,
        'joined': list_products[:5],
        'tbl': tab_marketability

    }

    return render(request, template_name="category.html", context=exit_)

def Get_Sales_Top(db_tbl, list_products, timelag=2, q=5):

    now = int(dt.strftime(dt.now(), "%m"))


    period_inbase = vlist_to_list(db_tbl['vardata'].objects.values_list('month').distinct().order_by())
    if None in period_inbase:
            period_inbase.remove(None)
    if len(period_inbase) < timelag:
         timelag=len(period_inbase)
    period_inbase = period_inbase[-timelag:]

    if list_products:
        qry_ = db_tbl['vardata'].objects.filter(month__in=period_inbase).\
            annotate(sales_timelag=Sum('sales_units')).\
            values('fk_products', 'sales_timelag').order_by('-sales_timelag')
    else:
        qry_ = 'ничо'

    return qry_