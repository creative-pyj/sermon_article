from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('search/', views.search_articles, name='search'),
    path('detail/<pk>/', views.get_detail, name='detail'),
]