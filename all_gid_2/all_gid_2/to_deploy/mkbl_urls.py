from django.urls import path

from django.views.generic.base import RedirectView, TemplateView
#from django.conf.urls.defaults import *

from . import views, txt_views

app_name = 'marketability'

handler404 = 'marketability.views.handler404'

urlpatterns = [
    path('', views.home, name="home"),
    path('how/', txt_views.how_Listing, name="how_list"),
    path('how/<slug:article>', txt_views.how_Article, name="how_article"),
    path('<slug:cat_>/', views.page_Category_Main, name='cat'),
    path('<slug:cat_>/<slug:product_>', views.page_Product, name='product'),
    path('al_about.html', views.about, name="about"),
    path('al_home.html', views.home, name="home"),
    path('search_all.html', views.search_all, name="doorway"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
    path('favicon.ico', RedirectView.as_view(url='/static/marketability/favicon.ico', permanent=True)),
]