from django.shortcuts import render
from django.http import HttpResponse
from .models import MntClasses, \
    MntProducts, \
    MntProductsHasMntClasses, \
    MntVardata, \
    NbClasses, \
    NbProducts, \
    NbProductsHasNbClasses, \
    NbVardata
from django import forms
from pprint import pprint


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
    str_CL = "<td valign=\"top\">" + td_type(dict['CL']) + "</td>"
    str_GO = "<td valign=\"top\">" + td_type(dict['GO']) + "</td>"
    str_footer = "</tr></table>"

    exit_ = str_header + str_CL + str_GO + str_footer

    with open("marketability/patterns/form.html", 'w', encoding='utf-8') as f:
        f.write(exit_)

    return exit_

def vlist_to_list(vlist):
    return [i[0] for i in vlist]

def page_Category_Main(request, post):

    category = dict_categories[post]
    db_tbl = category['db_tables']

    categories_list = [(dict_categories[cat]['category_name'], cat) for cat in dict_categories]

    form_fld = db_tbl['classes'].objects.all()
    list_enabled = vlist_to_list(list(form_fld.values_list('name')))

    if request.POST:
        #pprint(request.POST)
        post_return = list(request.POST.keys())
        print(post_return)
        post_return.remove('csrfmiddlewaretoken')
        print(post_return)

        kwargs_classes = {"fk_classes__name__in": post_return}
        pprint(kwargs_classes)
        joined_mtm = db_tbl['mtm_prod_clas'].objects.filter(**kwargs_classes).values('fk_products', 'fk_classes')
        products_mtm = db_tbl['mtm_prod_clas'].objects\
            .filter(fk_products__in=joined_mtm.values_list('fk_products'))\
            .order_by('fk_products')\
            .values('fk_products', 'fk_classes')
        products_for_execute = vlist_to_list(list(products_mtm.values_list('fk_products').distinct()))
        classes_for_execute = vlist_to_list(list(products_mtm.values_list('fk_classes').distinct()))
        #print(products_for_execute)
        list_enabled_ = db_tbl['classes'].objects.filter(id__in=classes_for_execute).values_list('name')
        list_enabled_ = vlist_to_list(list(list_enabled_))
        print(list_enabled_)
        if list_enabled_:
            enabled_return = list_enabled_
        else:
            enabled_return = list_enabled
        tbl_joined = {"1": 0, "2": 0}
    else:
        post_return = []
        enabled_return = list_enabled
        joined_mtm = "пусто"
        tbl_joined = {"1": 0, "2": 0}


    dict_form_fld = Dict_by_Classes(form_fld)
    html_form = Form_by_dict_classes(dict_form_fld, post_return, enabled_return)

    exit_ = {
        'category_name':  category['category_name'],
        'categories_list': categories_list,
        'action': post,
        'form': html_form,
        'joined': tbl_joined

    }

    return render(request, template_name="category.html", context=exit_)
