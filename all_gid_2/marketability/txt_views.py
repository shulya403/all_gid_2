from django.shortcuts import render
from . import views
from .models import TxtHow, TxtRatings

from datetime import datetime as dt

def how_Listing(request):

   listing = TxtHow.objects.all().values('idtxt_how', 'artice_title', 'article_anno')

   if listing:

       try:
           categories_list = request.session['categories_list']
       except KeyError:
           ctg = views.Init_cat(request, '', {})
           categories_list = request.session['categories_list']

       exit_ = {
           'categories_list': categories_list,
            'listing': listing
        }

       return render(request, template_name="ttx_how.html", context=exit_)
   else:
        return views.handler404(request)

def how_Article(request, article):

    article = TxtHow.objects.filter(idtxt_how=article).values()

    if article:

        try:
            categories_list = request.session['categories_list']
        except KeyError:
            ctg = views.Init_cat(request, '', {})
            categories_list = request.session['categories_list']

        exit_ = {
            'categories_list':  categories_list,
            'article': article[0]
        }

        return render(request, template_name="ttx_how_article.html", context=exit_)
    else:
        return views.handler404(request)
