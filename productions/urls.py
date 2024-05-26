"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from productions import views
urlpatterns = [
    path('create/', views.CreateProductionView.as_view()),
    path('create_item/', views.CreateProductionItemView.as_view()),
    path('get_product_by_id/', views.GetProductionByIdView.as_view()),
    path('get_products_by_pageid/', views.GetProductionsView.as_view()),
    path('get_productions_by_filters/', views.GetProductionsByFiltersView.as_view()),
    path('search_productions/', views.SearchProductionsView.as_view()),
    path('top_productions/', views.TopProductionsView.as_view()),
    path('update_product/', views.UpdateProductionView.as_view()),
    path('update_product_item/', views.UpdateProductionItemView.as_view()),
    path('get_category_list/', views.GetCategoryListView.as_view()),
]
