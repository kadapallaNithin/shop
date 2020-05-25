"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import ProductListView, BillListView, BillParticularsListView, BillCreateView, ParticularCreateView
from . import views
urlpatterns = [
    path('',views.index,name='home'),
#    path('cart/',views.cart,name='cart'),#see bill_particular
    path('products/',ProductListView.as_view(),name='products'),
    path('bills/',BillListView.as_view(),name='bills'),
    path('particular/',ParticularCreateView.as_view(),name='particular'),
    path('new-bill',BillCreateView.as_view(),name='new_bill'),
    path('bill/<int:id>/',BillParticularsListView.as_view(),name='bill_particular')
]