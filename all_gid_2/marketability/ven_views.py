from django.shortcuts import render
from . import views
import time


def vendor(request, cat_, vendor_=""):

    start_time = time.monotonic()

    db_tbl = views.DB_table(cat_)

    try:
        categories_list = request.session['categories_list']

    except KeyError:
        ctg = views.Init_cat(request, cat_, db_tbl)
        categories_list = request.session['categories_list']
    str_period_inbase = request.session['period_inbase']
    period_inbase = views.Recover_Date_period_inbase(str_period_inbase)

    if not vendor_:
        vendor_ = db_tbl['products'].objects.values_list('brand').distinct()[0][0]


    #qry = db_tbl['products'].objects.filter(id=2653)[0].classes_mtm.values('name')
    GeneralQry = db_tbl['products'].objects.filter(brand=vendor_, nbvardata__month__in=period_inbase).values()
    print(len(GeneralQry))
    qry = db_tbl['products'].objects.prefetch_related('classes_mtm').values('name', 'classes_mtm__text')
    print(qry[0:10])

    #start_time = time.monotonic()
    list_classes_GO = list()
    for subtype in request.session['new_form']['GO']:
        for clg in [cl['text'] for cl in request.session['new_form']['GO'][subtype]]:
                list_classes_GO.append(clg)
    print(list_classes_GO)

    start_time = time.monotonic()
    for goal in list_classes_GO:
        for i in range(len(GeneralQry)):
            GeneralQry[i][goal] = (goal in views.vlist_to_list(qry.filter(name=GeneralQry[i]['name']).values_list('classes_mtm__text')))
    print(time.monotonic()-start_time)
    print(GeneralQry[0])


    # for i, g_qry in enumerate(GeneralQry):
    #     name_ = g_qry['name']
    #     for goal in list_classes_GO:
    #         GeneralQry[i][goal] = len(qry.filter(name=name_, classes_mtm__text=goal))
    #         if i == 0:
    #             print(qry.filter(name=name_, classes_mtm__text=goal))
    # print(time.monotonic()-start_time)
    # print(GeneralQry[0])

    return render(request, template_name="ttx_how.html", context={})