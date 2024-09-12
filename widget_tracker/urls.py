from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.config, name='config'),
    path('pages/', views.pages, name='pages'),
    path('identify/', views.identify, name='identify'),
    path('form/', views.form, name='form'),
    path('pixel/', views.pixel, name='pixel'),
]