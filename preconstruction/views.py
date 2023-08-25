import re
from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from .models import Developer, PreConstruction, PreConstructionImage, City, PreConstructionFloorPlan, Event, News, Favourite
from rest_framework.pagination import PageNumberPagination
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import math
import csv
from accounts.models import Agent
import datetime
from rest_framework import generics
from .serializers import *


class DeveloperListCreateView(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class DeveloperRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class PreConstructionListCreateView(generics.ListCreateAPIView):
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer


class PreConstructionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class FavouriteListCreateView(generics.ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class FavouriteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
