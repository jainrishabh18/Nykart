# 
from django.urls import path
from .import views
urlpatterns =[
    #  slug is url of different different categories
    path('', views.store, name='store'),

    # slug will take url for the category we are seaching for and show us product of that category
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),

    # taking two slug category_slug and product_slug  of that category
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    
    path('search/',views.search, name='search'),
]
