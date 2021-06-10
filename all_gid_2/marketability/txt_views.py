from django.shortcuts import render
from . import views
from .models import TxtHow, TxtRatings

from datetime import datetime as dt

def how_Listing(request):

    total_txt_how = TxtHow.objects.all().values('idtxt_how', 'artice_title', 'cat', 'article_anno', 'img', 'pin', 'date')

    try:
           categories_list = request.session['categories_list']

    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']

    listing = dict()
    for cat_ in  categories_list:
        print(cat_)
        listing_cat = total_txt_how.filter(cat=cat_[1]).order_by('pin', 'date')
        print(listing_cat)
        if len(listing_cat) > 0:
               listing[cat_[0]] = listing_cat


    exit_ = {
           'categories_list': categories_list,
            'listing': listing
        }

    return render(request, template_name="ttx_how.html", context=exit_)

def how_cat_Listing(request, cat_):

    listing = TxtHow.objects.filter(cat=cat_).values('idtxt_how', 'artice_title', 'article_anno', 'img', 'pin', 'date')

    ctg = views.Init_cat(request, '', {})

    try:
           categories_list = request.session['categories_list']
           categories_list_singular = request.session['categories_list_singular']
    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']
           categories_list_singular = request.session['categories_list_singular']



    exit_ = {
           'categories_list': categories_list,
           'categories_list_singular': categories_list_singular[cat_],
           'listing': listing,
           'cat': cat_
        }

    return render(request, template_name="ttx_how_cat.html", context=exit_)

def how_Article(request, cat_, article):

    article = TxtHow.objects.filter(idtxt_how=article).values()

    if article:

        try:
            categories_list = request.session['categories_list']
        except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

        exit_ = {
            'categories_list':  categories_list,
            'article': article[0],
            'category': cat_
        }

        return render(request, template_name="ttx_how_article.html", context=exit_)
    else:
        return views.handler404(request)

def rate_Listing(request):

    total_txt_rate = TxtRatings.objects.all().values('idtxt_ratings', 'article_title', 'cat', 'article_anno', 'img', 'pin', 'date')

    try:
           categories_list = request.session['categories_list']

    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']

    listing = dict()
    for cat_ in  categories_list:
        print(cat_)
        listing_cat = total_txt_rate.filter(cat=cat_[1]).order_by('pin', 'date')
        print(listing_cat)
        if len(listing_cat) > 0:
               listing[cat_[0]] = listing_cat


    exit_ = {
           'categories_list': categories_list,
            'listing': listing
        }

    return render(request, template_name="ttx_rate.html", context=exit_)

def rate_cat_Listing(request, cat_):

    listing = TxtRatings.objects.filter(cat=cat_).values('idtxt_ratings', 'article_title', 'article_anno', 'img', 'pin', 'date')

    ctg = views.Init_cat(request, '', {})

    try:
           categories_list = request.session['categories_list']
           categories_list_singular = request.session['categories_list_singular']
    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']
           categories_list_singular = request.session['categories_list_singular']



    exit_ = {
           'categories_list': categories_list,
           'categories_list_singular': categories_list_singular[cat_],
           'listing': listing,
           'cat': cat_
        }

    return render(request, template_name="ttx_rate_cat.html", context=exit_)

def rate_Article(request, cat_, article):

    article = TxtRatings.objects.filter(idtxt_ratings=article).values()

    if article:

        try:
            categories_list = request.session['categories_list']
        except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

        cat_rus = [ct[0] for ct in categories_list if ct[1] == cat_][0]
        exit_ = {
            'categories_list':  categories_list,
            'article': article[0],
            'category': cat_,
            'cat_rus': cat_rus

        }

        return render(request, template_name="ttx_rate_article.html", context=exit_)
    else:
        return views.handler404(request)



