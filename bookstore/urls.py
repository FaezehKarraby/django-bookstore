from django.urls import path
from . import views

app_name = 'bookstore'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.index_api),
    path('about/', views.about, name='about'),
    path('genre/<int:gn>/', views.genre, name='genre'),
    path('api/genre/<int:gn>/', views.genre_api),
]
