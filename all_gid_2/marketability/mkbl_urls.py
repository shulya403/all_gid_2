from django.urls import path

from django.views.generic.base import RedirectView
#from django.conf.urls.defaults import *

from . import views

app_name = 'marketability'

urlpatterns = [
    path('', RedirectView.as_view(url='/Nb/')),
    path('<slug:cat_>/', views.page_Category_Main, name='cat'),
#    path('1/<slug:cat_>/', views.AllgidBase.as_view(), name='test')
]