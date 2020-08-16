from django.urls import path

from django.views.generic.base import RedirectView
#from django.conf.urls.defaults import *

from . import views

app_name = 'marketability'

urlpatterns = [
    path('', RedirectView.as_view(url='/Nb/')),
    path('<slug:post>/', views.page_Category_Main, name='cat')
]