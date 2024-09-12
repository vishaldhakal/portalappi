from django.urls import path
from .views import ConfigView, PageView, IdentifyView, FormView, pixel

urlpatterns = [
    path('config/', ConfigView.as_view(), name='config'),
    path('pages/', PageView.as_view(), name='pages'),
    path('identify/', IdentifyView.as_view(), name='identify'),
    path('form/', FormView.as_view(), name='form'),
    path('pixel/', pixel, name='pixel'),
]