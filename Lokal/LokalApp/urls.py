"""Lokal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from LokalApp import views

app_name = 'Lokalapp'

urlpatterns = [
    path('index', views.myIndexView.as_view(), name="my_index_view"),
    path('dashboard', views.myDashboardView.as_view(), name="my_dashboard_view"),
    path('contactUs', views.myContactUsView.as_view(), name="my_contactUs_view"),
    path('about/',views.about),
    #path('about', views.myAboutView.as_view(), name="my_about_view"),
    path('feature', views.myFeatureView.as_view(), name="my_feature_view"),
    path('login', views.LoginView.as_view(), name="my_login_view"),
    path('logout', views.logout_view, name="my_logout_view"),
    
    path('signup/', views.SignUp),  
    path('addUser', views.myAddUserView.as_view(), name="my_addUser_view"),
    path('addProduct', views.myAddProductView.as_view(), name="my_addProduct_view"),
    path('addType', views.myAddTypeView.as_view(), name="my_addType_view"),
    path('delete_customer/<str:username>', views.delete_customer, name="delete_customer"),
    path('delete_product/<int:item_code>', views.delete_product, name="delete_product"),
    path('delete_product_type/<int:type_code>', views.delete_product_type, name="delete_product_type"),
    path('edit_customer/<str:username>', views.edit_customer, name="edit_customer"),
    path('edit_product/<int:item_code>', views.edit_product, name="edit_product"),
    path('edit_menu_type/<int:type_code>', views.edit_product_type, name="edit_product_type"),
    path('add_to_cart/<int:item_code>', views.add_to_cart, name="add_to_cart"),
    path('remove_to_cart/<int:item_code>', views.remove_to_cart, name="remove_to_cart"),
    path('qtyCounter/<int:item_code>', views.qtyCounter, name="qtyCounter"),
    path('cart', views.myCartView.as_view(), name="my_cart_view"),
   
]
