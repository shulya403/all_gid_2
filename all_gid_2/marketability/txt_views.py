from django.shortcuts import render
from . import views
from .models import TxtHow, TxtRatings

from datetime import datetime as dt

def how_Listing(request):

    total_txt_how = TxtHow.objects.all().values('idtxt_how', 'id_html_name', 'article_title', 'cat', 'article_anno', 'img', 'pin', 'date')

    try:
           categories_list = request.session['categories_list']

    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']

    listing = dict()
    for cat_ in  categories_list:
        print(cat_)
        listing_cat = total_txt_how.filter(cat=cat_[1]).order_by('pin', '-date')
        print(listing_cat)
        if len(listing_cat) > 0:
               listing[cat_[0]] = listing_cat


    exit_ = {
           'categories_list': categories_list,
            'listing': listing,
            'txt': 'how'
        }

    return render(request, template_name="ttx_how.html", context=exit_)

def how_cat_Listing(request, cat_):

    listing = TxtHow.objects.filter(cat=cat_).values('idtxt_how', 'id_html_name', 'article_title', 'article_anno', 'img', 'pin', 'date')

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
           'categories_name_plural': [name[0] for name in categories_list if name[1] == cat_][0],
           'listing': listing,
           'cat': cat_,
           'txt': 'how'
        }

    return render(request, template_name="ttx_how_cat.html", context=exit_)

def how_Article(request, cat_, article):

    article = TxtHow.objects.filter(id_html_name=article).values()

    if article:

        try:
            categories_list = request.session['categories_list']
        except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

        cat_rus = [ct[0] for ct in categories_list if ct[1] == cat_][0]
        exit_ = {
            'categories_list':  categories_list,
            'categories_name_plural': [name[0] for name in categories_list if name[1] == cat_][0],
            'article': article[0],
            'category': cat_,
            'cat_rus': cat_rus,
            'txt': 'how'

        }

        return render(request, template_name="ttx_how_article.html", context=exit_)
    else:
        return views.handler404(request)

def rate_Listing(request):

    total_txt_rate = TxtRatings.objects.all().values('idtxt_ratings', 'id_html_name', 'article_title', 'cat', 'article_anno', 'img', 'pin', 'date')

    try:
           categories_list = request.session['categories_list']

    except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']

    listing = dict()
    for cat_ in  categories_list:
        listing_cat = total_txt_rate.filter(cat=cat_[1]).order_by('pin', '-date')
        if len(listing_cat) > 0:
               listing[cat_[0]] = listing_cat


    exit_ = {
           'categories_list': categories_list,
            'listing': listing,
            'txt': 'rate'
        }

    return render(request, template_name="ttx_rate.html", context=exit_)

def rate_cat_Listing(request, cat_):

    listing = TxtRatings.objects.filter(cat=cat_).values('idtxt_ratings', 'id_html_name', 'article_title', 'article_anno', 'img', 'pin', 'date').order_by('pin', '-date')

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
           'categories_name_singular': categories_list_singular[cat_],
           'categories_name_plural': [name[0] for name in categories_list if name[1] == cat_][0],
           'listing': listing,
           'cat': cat_,
            'txt': 'rate'

        }

    return render(request, template_name="ttx_rate_cat.html", context=exit_)

def rate_Article(request, cat_, article):

    article = TxtRatings.objects.filter(id_html_name=article).values()

    if article:

        try:
            categories_list = request.session['categories_list']
        except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

        cat_rus = [ct[0] for ct in categories_list if ct[1] == cat_][0]
        exit_ = {
            'categories_list':  categories_list,
            'categories_name_plural': [name[0] for name in categories_list if name[1] == cat_][0],
            'article': article[0],
            'category': cat_,
            'cat_rus': cat_rus,
            'txt': 'rate'

        }

        return render(request, template_name="ttx_rate_article.html", context=exit_)
    else:
        return views.handler404(request)

def RSS_Rate(request):

    articles = TxtRatings.objects.all()

    try:
            categories_list = request.session['categories_list']
    except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

    for i, article in enumerate(articles):
        articles[i].pub_date = dt.strftime(article.date, "%a, %d %b %Y 08:00:00 +0300")
        articles[i].cat_plural = [name[0] for name in categories_list if name[1] == article.cat][0]

    exit_ = {
        'categories_list': categories_list,
        "channel_title": "Гид покупателя. Рейтинги. Мониторы, Ноутбуки, Принтеры и МФУ, ИБП, ",
        "channel_description": "Рейтинги. Top самых популярных моделей в России. Обзоры и подборки. Лучшие Мониторы, Ноутбуки, Принтеры и МФУ, ИБП, ",

        "items": articles

    }

    #rendered = render_to_string('rss-turbo.xml', exit_)

    return render(request, template_name="rss-turbo.xml", context=exit_, content_type="application/rss-xml")

def RSS_How(request):

    articles = TxtHow.objects.all()

    try:
            categories_list = request.session['categories_list']
    except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

    for i, article in enumerate(articles):
        articles[i].pub_date = dt.strftime(article.date, "%a, %d %b %Y 08:00:00 +0300")
        articles[i].cat_plural = [name[0] for name in categories_list if name[1] == article.cat][0]

    exit_ = {
        'categories_list': categories_list,
        "channel_title": "Гид покупателя. Как выбрать. Мониторы, Ноутбуки, Принтеры и МФУ, ИБП",
        "channel_description": "Советы по выбору. Обзоры и подборки. Лучшие Мониторы, Ноутбуки, Принтеры, МФУ, ИБП",

        "items": articles

    }

    #rendered = render_to_string('rss-turbo.xml', exit_)

    return render(request, template_name="rss-turbo-how.xml", context=exit_, content_type="application/rss-xml")


