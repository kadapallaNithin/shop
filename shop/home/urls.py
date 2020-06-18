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
from .views import PaymentCreateView, ProductListView, BillListView, BillParticularsListView, CustomerBillsListView, CustomerListView, CustomerUpdateView, ParticularCreateView, InvoiceListView, PaymentsListView#, CustomerCreateView, VillageCreateView # BillCreateView,
from . import views
urlpatterns = [
    path('payment/<int:bill_id>/',views.payment,name='payment'),
#    path('payment/<int:bill_id>/',PaymentCreateView.as_view(),name='payment'),
    path('payments/',PaymentsListView.as_view(),name='payments'),
    #path('payments/',views.payment_list,name='payments'),
#    path('cart/',views.cart,name='cart'),#see bill_particular
    path('products/',ProductListView.as_view(),name='products'),
    path('bills/',BillListView.as_view(),name='bills'),
#    path('customer/add/',CustomerCreateView.as_view(),name='add_customer'),
    path('customer/<int:id>/bills/',CustomerBillsListView.as_view(),name='customer_bills'),
    path('customers/',CustomerListView.as_view(),name='customers'),
    path('customer/<int:pk>/',CustomerUpdateView.as_view(),name='customer_update'),
    path('particular/',ParticularCreateView.as_view(),name='particular'),
    path('new_particular/<int:bill_id>/',views.add_particular,name='new_particular'),
    path('',views.bill_create,name='new_bill'),#BillCreateView.as_view()
    path('bill/<int:id>/',BillParticularsListView.as_view(),name='bill_particular'),
    path('new_invoice/',views.invoice,name='new_invoice'),
    #path('new_invoice/',views.InvoiceCreate.view,name='new_invoice'),
    path('invoices/',InvoiceListView.as_view(),name='invoices'),
    path('new_rate/<int:prod_id>/',views.rate_create,name='new_rate'),
    path('export/<str:model_name>',views.export,name='export'),
    path('export_list/',views.export_list,name='export_list'),
    path('export_all/',views.export_all,name='export_all'),
    path('village/',views.village_create,name='new_village'),
    path('villages/',views.village_list,name='villages'),
]