from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('advanced-search/', views.advanced_search,
         name='advanced_search'),
    path('advanced-search/results/',
         views.advanced_results, name='advanced_results'),
    path('results/', views.results, name='results'),
]
