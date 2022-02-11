from django.urls import path

from django.views.generic.base import RedirectView, TemplateView
#from django.conf.urls.defaults import *

from . import views, views_new, txt_views_new

app_name = 'marketability'

handler404 = 'marketability.views.handler404'

urlpatterns = [
    path('', views.home, name="home"),
    path('how/', txt_views_new.how_Listing, name="how_list"),
    path('how/<slug:cat_>/', txt_views_new.how_cat_Listing, name="how_cat_listing"),
    path('how/<slug:cat_>/<slug:article>', txt_views_new.how_Article, name="how_article"),
    path('rate/', txt_views_new.rate_Listing, name="how_list"),
    path('rate/<slug:cat_>/', txt_views_new.rate_cat_Listing, name="how_cat_listing"),
    path('rate/<slug:cat_>/<slug:article>', txt_views_new.rate_Article, name="how_article"),
    path('<slug:cat_>/', views_new.page_Category_Main, name='cat'),
    path('<slug:cat_>/<slug:product_>', views_new.page_new_Product, name='product'),
    path('al_about.html', views_new.about, name="about"),
    path('al_home.html', views_new.home, name="home"),
    path('search_all.html', views_new.search_all, name="doorway"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('ads.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
    path('favicon.ico', RedirectView.as_view(url='/static/marketability/favicon.ico', permanent=True)),
    path('rss-turbo.xml', txt_views_new.RSS_Rate),
    path('rss-turbo-how.xml', txt_views_new.RSS_How)
]