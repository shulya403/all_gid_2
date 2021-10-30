from django.shortcuts import render
from . import views
import time


def vendor(request, cat_, vendor_=""):

    start_time = time.monotonic()

    db_tbl = views.DB_table(cat_)

    try:
        categories_list = request.session['categories_list']
        category_name = request.session['cat_rus_name']

    except KeyError:
        ctg = views.Init_cat(request, cat_, db_tbl)
        categories_list = request.session['categories_list']
        category_name = request.session['cat_rus_name']
    str_period_inbase = request.session['period_inbase']
    period_inbase = views.Recover_Date_period_inbase(str_period_inbase)

    vardata_kwargs = {cat_.lower() + 'vardata__month__in': period_inbase}
    vendors_list = db_tbl['products'].objects.filter(**vardata_kwargs).values_list(
        'brand').distinct().order_by('brand')
    print(vendors_list)

    if not vendor_:
        vendor_ = views.vlist_to_list(vendors_list)[0]
        print(vendor_)


    #qry = db_tbl['products'].objects.filter(id=2653)[0].classes_mtm.values('name')
    brand_vardata_kwargs = {'brand': vendor_, cat_.lower() + 'vardata__month__in': period_inbase}
    GeneralQry = db_tbl['products'].objects.filter(**brand_vardata_kwargs).values()
    print(len(GeneralQry))
    #qry = db_tbl['products'].objects.prefetch_related('classes_mtm').values('name', 'classes_mtm__text')
    #print(qry[0:10])

    #start_time = time.monotonic()
    list_classes_GO_CL = list()
    for subtype in request.session['new_form']['GO']:
        for clg in [cl['text'] for cl in request.session['new_form']['GO'][subtype]]:
                list_classes_GO_CL.append(clg)
    for subtype in request.session['new_form']['CL']:
        for clg in [cl['text'] for cl in request.session['new_form']['CL'][subtype]]:
            list_classes_GO_CL.append(clg)

    print(list_classes_GO_CL)

    start_time = time.monotonic()
    #classes_mtm_list = views.vlist_to_list(qry.filter(name=GeneralQry[0]['name']).values_list('classes_mtm__text'))
    #print(classes_mtm_list)
    for goal in list_classes_GO_CL:
        for i in range(len(GeneralQry)):
            GeneralQry[i][goal] = (goal in list_classes_GO_CL)
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
    fieleds_ttx = list()
    for fld in GeneralQry[0].keys():
        if fld not in (set(list_classes_GO_CL) | {'id', 'brand'}):
            fieleds_ttx.append(fld)

    exit_ = {
        'categories_list': categories_list,
        'category_name': category_name,
        'action': cat_,
        'vendors_list': views.vlist_to_list(vendors_list),
        'vendor': vendor_,
        'table': GeneralQry,
        'fieleds_ttx': fieleds_ttx,
        'fields_classes': list_classes_GO_CL
    }

    return render(request, template_name="vendors.html", context=exit_)