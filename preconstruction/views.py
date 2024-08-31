import re
from rest_framework import status
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from .models import Developer, PreConstruction, PreConstructionImage, City, PreConstructionFloorPlan, Event, News, Favourite,Partner,LeadsCount,TrackingEvent
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
from django.utils.text import slugify
""" import asyncio
from sydney import SydneyClient

sydney = SydneyClient()

async def clientt(prompt) -> str:
    async with SydneyClient() as sydney:
        print(prompt)
        if prompt == "!reset":
            await sydney.reset_conversation()
            return "Conversation reset"
        elif prompt == "!exit":
            return "Goodbye"
        else:
            newp = prompt+ " answer it under 250 letters"
            responses = []
            async for response in sydney.ask_stream(newp):
                responses.append(response)
            
            return ''.join(responses)

@api_view(['POST'])
def robotView(request):
    data = request.data
    prompt = data.get("prompt")
    return Response({"message": asyncio.run(clientt(prompt))})
 """

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000

class DeveloperListCreateView(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    pagination_class = LargeResultsSetPagination


class DomainsListCreateView(generics.ListCreateAPIView):
    queryset = Domains.objects.all()
    serializer_class = DomainsSerializer

class DomainsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Domains.objects.all()
    serializer_class = DomainsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.domain = request.data.get('domain')
        instance.contact_email = request.data.get('contact_email')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


#create a function which receives domain as input from url as get request and returns the domain details
@api_view(['GET'])
def get_domain(request):
    domainn = request.GET["domain"]
    domain = Domains.objects.get(domain=domainn)
    serializer = DomainsSerializer(domain)
    return Response(serializer.data)

class DeveloperRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('image'):
            instance.image = request.data.get('image')
        instance.name = request.data.get('name')
        instance.details = request.data.get("details")
        instance.website_link = request.data.get('website_link')
        instance.phone = request.data.get('phone')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class PreConstructionListCreateView(generics.ListCreateAPIView):
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        is_featured = request.GET.get('is_featured',False)
        city = request.GET.get('city','All')
        page_size = request.GET.get('page_size',60)
        smallerv = request.GET.get('small','All')

        if is_featured:
            preconstructions = PreConstruction.objects.filter(is_featured=True)
        else:
            preconstructions = PreConstruction.objects.all()
        
        if city != 'All':
            preconstructions = preconstructions.filter(city__slug=city)
        


        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(preconstructions, request)
        
        if smallerv != "All":
            serializer = PreConstructionSerializerSmallVsmall(result_page, many=True)
        else:
            serializer = PreConstructionSerializerSmall(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        data = request.data
        developer_id = data.get('predata[developer][id]')
        city_id = data.get('predata[city][id]')
        developer = Developer.objects.get(id=developer_id)
        city = City.objects.get(id=city_id)
        project_name = data.get('predata[project_name]')

        project_type = data.get('predata[project_type]')
        is_featured = data.get('predata[is_featured]')
        status = data.get('predata[status]')
        project_address = data.get('predata[project_address]')
        description = data.get('predata[description]')
        co_op = data.get('predata[co_op_available]')
        co_op_available = True if co_op == "true" else False
        price_starting_from = data.get('predata[price_starting_from]')
        price_to = data.get('predata[price_to]')
        occupancy = data.get('predata[occupancy]')
        no_of_units = data.get('predata[no_of_units]')

        """Generate slug from project name with unique in case of same name"""
        slug = slugify(project_name)
        if PreConstruction.objects.filter(slug=slug).exists():
            slug = f'{slug}-{PreConstruction.objects.all().count()}'

        preconstruction = PreConstruction.objects.create(
            developer=developer,
            city=city,
            project_name=project_name,
            slug=slug,
            project_type=project_type,
            status=status,
            project_address=project_address,
            description=description,
            co_op_available=co_op_available,
            price_starting_from=price_starting_from,
            price_to=price_to,
            occupancy=occupancy,
            no_of_units=no_of_units
        )

        if is_featured == "true":
            preconstruction.is_featured = True
        else:
            preconstruction.is_featured = False

        """ Save images from images received """
        images = request.data.getlist('images[]')

        for image in images:
            PreConstructionImage.objects.create(
                preconstruction=preconstruction, image=image)

        """ Save floorplans """
        floorplans = request.data.getlist('plans[]')
        for floorplan in floorplans:
            PreConstructionFloorPlan.objects.create(
                preconstruction=preconstruction, floorplan=floorplan)

        preconstruction.save()
        serializer = PreConstructionSerializer(preconstruction)
        return Response(serializer.data)


class PreConstructionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PreConstruction.objects.all()
    serializer_class = PreConstructionSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        developer_id = data.get('predata[developer][id]')
        city_id = data.get('predata[city][id]')
        developer = Developer.objects.get(id=developer_id)
        city = City.objects.get(id=city_id)
        project_name = data.get('predata[project_name]')
        project_type = data.get('predata[project_type]')
        status = data.get('predata[status]')
        project_address = data.get('predata[project_address]')
        description = data.get('predata[description]')
        co_op = data.get('predata[co_op_available]')
        co_op_available = True if co_op == "true" else False
        price_starting_from = data.get('predata[price_starting_from]')
        price_to = data.get('predata[price_to]')
        occupancy = data.get('predata[occupancy]')
        no_of_units = data.get('predata[no_of_units]')
        is_featured = data.get('predata[is_featured')

        if is_featured == "true":
            instance.is_featured = True
        else:
            instance.is_featured = False

        instance.developer = developer
        instance.city = city
        instance.project_name = project_name
        instance.project_type = project_type
        instance.status = status
        instance.project_address = project_address
        instance.description = description
        instance.co_op_available = co_op_available
        instance.price_starting_from = price_starting_from
        instance.price_to = price_to
        instance.occupancy = occupancy
        instance.no_of_units = no_of_units

        if instance.slug != slugify(project_name):
            if PreConstruction.objects.filter(slug=slugify(project_name)).exists():
                instance.slug = slugify(project_name) + "-" + str(instance.id)
            else:
                instance.slug = slugify(project_name)

        """ Save images """
        images = request.FILES.getlist('images[]')
        for image in images:
            PreConstructionImage.objects.create(
                preconstruction=instance, image=image)

        """ Save floorplans """
        floorplans = request.FILES.getlist('plans[]')
        for floorplan in floorplans:
            PreConstructionFloorPlan.objects.create(
                preconstruction=instance, floorplan=floorplan)

        instance.save()
        serializer = PreConstructionSerializer(instance)
        return Response(serializer.data)


@api_view(['GET'])
def get_related_precons(request, city):
    precons = PreConstruction.objects.filter(city__slug=city)[:4]
    serializer = PreConstructionSerializerSmall(precons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def remove_last_part_of_slug(request):
    precons = PreConstruction.objects.all()
    for precon in precons:
        slug = precon.slug.split('-')
        # check if last part is no
        if re.match(r'\d+', slug[-1]):
            new_str = '-'.join(slug[:-1])
            if PreConstruction.objects.filter(slug=new_str).exists():
                new_str = new_str + "-" + str(precon.id)
            precon.slug = new_str
            precon.save()
    return Response({"message": "done"})


@api_view(['GET'])
def PreConstructionDetailView(request, slug):
    preconstruction = PreConstruction.objects.get(slug=slug)
    serializer = PreConstructionSerializer(preconstruction)
    cityyy = preconstruction.city
    partt = Partner.objects.filter(cities=cityyy)
    serializer2 = PartnerSerializer(partt, many=True)
    return Response({"preconstruction": serializer.data,"partner":serializer2.data})

@api_view(['GET'])
def PreConstructionsCityView(request, slug):
    status = request.GET.get('status')
    page_size = request.GET.get('page_size',60)
    occupancy = request.GET.get('occupancy')
    project_type = request.GET.get('project_type')
    is_featured = request.GET.get('is_featured')
    price_starting_from = request.GET.get('price_starting_from')
    city = City.objects.get(slug=slug)
    cityser = CitySerializer(city)

    partt = Partner.objects.filter(cities=city)
    serializer2 = PartnerSerializer(partt, many=True)

    if is_featured:
        preconstructions = PreConstruction.objects.filter(city__slug=slug,is_featured=True).order_by('-is_featured','-last_updated')
    else:
        preconstructions = PreConstruction.objects.filter(city__slug=slug,is_featured=False).order_by('-is_featured','-last_updated')
        
    #add pagination
    paginator = PageNumberPagination()
    paginator.page_size = page_size

    if status:
        preconstructions = preconstructions.filter(status=status)
    if occupancy:
        preconstructions = preconstructions.filter(occupancy=occupancy)
    if project_type:
        preconstructions = preconstructions.filter(project_type=project_type)
    if price_starting_from:
        preconstructions = preconstructions.filter(
            price_starting_from__gte=price_starting_from)

    preconstructions = paginator.paginate_queryset(preconstructions, request)
        
    serializer = PreConstructionSerializerSmall(preconstructions, many=True)
    return Response({"city": cityser.data, "preconstructions": serializer.data,"partner":serializer2.data})



class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class PartnerListCreateView(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        image = request.FILES['image']
        name = data.get('name')
        email = data.get('email')
        brokerage_name = data.get('brokerage_name')
        
        cities_data = []
        for key, value in data.items():
            if key.startswith('cities['):
                city_index = int(key.split('[')[1].split(']')[0])
                city_field = key.split(']')[1][1:]
                if city_index >= len(cities_data):
                    cities_data.append({})
                cities_data[city_index][city_field] = value

        partner = Partner.objects.create(
            name=name, email=email, brokerage_name=brokerage_name, image=image)
        
        for city_data in cities_data:
            city = City.objects.get(name=city_data['name'])
            partner.cities.add(city)

        partner.save()
        serializer = PartnerSerializer(partner)
        return Response(serializer.data)


class PartnerRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('image'):
            instance.image = request.data.get('image')

        instance.name = request.data.get('name')
        instance.email = request.data.get('email')
        instance.brokerage_name = request.data.get('brokerage_name')

        cities_data = []
        for key, value in request.data.items():
            if key.startswith('selectedCities['):
                city_index = int(key.split('[')[1].split(']')[0])
                city_field = key.split(']')[1][1:]
                if city_index >= len(cities_data):
                    cities_data.append({})
                cities_data[city_index][city_field] = value

        instance.cities.clear()
        instance.save()
        for city_data in cities_data:
            city = City.objects.get(name=city_data['name'])
            instance.cities.add(city)

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        city_data = data.get('city[name]')
        try:
            city = City.objects.get(name=city_data)
        except City.DoesNotExist:
            return Response({"message": "City not found"}, status=status.HTTP_400_BAD_REQUEST)

        print(data.get('news_thumbnail'))
        news_title = data.get('news_title')
        news_thumbnail = data.get('news_thumbnail')
        news_description = data.get('news_description')
        news_link = data.get('news_link')
        slug = slugify(news_title)

        news = News.objects.create(
            city=city,
            news_title=news_title,
            news_thumbnail=news_thumbnail,
            news_description=news_description,
            news_link=news_link,
            slug=slug
        )
        serializer = NewsSerializer(news)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        city = request.GET.get('city')
        if city:
            news = News.objects.filter(city__slug=city)
        else:
            news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)


class NewsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city_data = request.data.get('city[name]')
        try:
            city = City.objects.get(name=city_data)
        except City.DoesNotExist:
            return Response({"message": "City not found"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('news_thumbnail'):
            instance.news_thumbnail = request.data.get('news_thumbnail')
        instance.news_title = request.data.get('news_title')
        instance.news_description = request.data.get('news_description')
        instance.news_link = request.data.get('news_link')
        instance.city = city
        if instance.slug != slugify(request.data.get('news_title')):
            if Developer.objects.filter(slug=slugify(request.data.get('news_title'))).exists():
                instance.slug = slugify(request.data.get('news_title')) + "-" + str(instance.id)
            else:
                instance.slug = slugify(request.data.get('news_title'))
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@api_view(['GET'])
def news_detail(request, slug):
    news = News.objects.get(slug=slug)
    serializer = NewsSerializer(news)
    return Response(serializer.data)

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = LargeResultsSetPagination

    """ custom function to create city with only name """

    def list(self, request, *args, **kwargs):
        show_desc = request.GET.get('show_desc', "Yes")
        page_size = request.GET.get('page_size', 10)
        cities = City.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(cities, request)
        if show_desc == "Yes":
            serializer = CitySerializer(result_page, many=True)
        else:
            serializer = CitySerializerSmall(result_page, many = True)

        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        city_name = data.get('name')
        city_details = data.get('details')
        base_slug = slugify(city_name)
        unique_slug = base_slug
        num = 1
        while City.objects.filter(slug=unique_slug).exists():
            unique_slug = base_slug + "-" + str(num)
            num += 1
        city = City.objects.create(
            name=city_name, slug=unique_slug, details=city_details)
        serializer = CitySerializer(city)
        return Response(serializer.data)


class CityRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get('name')
        city_details = request.data.get('details')
        base_slug = slugify(request.data.get('name'))
        unique_slug = base_slug
        instance.slug = unique_slug
        instance.details = city_details
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FavouriteListCreateView(generics.ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class FavouriteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


@api_view(['DELETE'])
def delete_image(request, pk):
    image = PreConstructionImage.objects.get(id=pk)
    image.delete()
    return JsonResponse("Deleted Successfully", safe=False)


@api_view(['DELETE'])
def delete_floorplan(request, pk):
    floorplan = PreConstructionFloorPlan.objects.get(id=pk)
    floorplan.delete()
    return JsonResponse("Deleted Successfully", safe=False)


@api_view(['GET'])
def get_all_city(request):
    cities = City.objects.all()
    serializer = CitySerializerSmall(cities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_precons_search(request):
    precons = PreConstruction.objects.all()
    serializer = PreConstructionSearchSerializer(precons, many=True)

    cities = City.objects.all()
    serializer2 = CitySerializerSmall(cities,many=True)

    return Response({"projects": serializer.data, "cities": serializer2.data})

@api_view(['GET'])
def get_all_precons(request):
    cities = City.objects.all()
    serializer = CitySerializerSmallSearch(cities, many=True)
    return Response(serializer.data)

def validate_name(name):
    """
    Validates the name field.
    Returns True if name is valid, False otherwise.
    """
    if not name:
        return False
    # Add additional name validation logic here if needed
    return True


def validate_email(email):
    """
    Validates the email field.
    Returns True if email is valid, False otherwise.
    """
    if not email:
        return False
    if '@' not in email:
        return False
    # Add additional email validation logic here if needed
    return True


def validate_phone(phone):
    """
    Validates the phone field.
    Returns True if phone is valid, False otherwise.
    """
    if not phone:
        return False
    # Add additional phone validation logic here if needed
    return True


def validate_message(message):
    """
    Validates the message field.
    Returns True if message is valid, False otherwise.
    """
    if not message:
        return False
    # Add additional message validation logic here if needed
    return True


@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        subject = "Inquiry about " + \
            request.POST["proj_name"]+" in " + \
            request.POST["cityy"]+" - Condomonk"
        emaill = "Condomonk <info@condomonk.ca>"
        headers = {'Reply-To': request.POST["email"]}

        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        realtor = request.POST["realtor"]

        if validate_name(request.POST["name"]) and validate_email(request.POST["email"]) and validate_phone(request.POST["phone"]):
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\nIs a realtor?: {realtor}"
            
            city = request.POST["cityy"]

            if City.objects.filter(name=city).exists():
                sss = city.replace("-", " ")
                slug_city = sss.title()
                cit = City.objects.get(name=slug_city)

                partnerss = Partner.objects.filter(cities=cit)
                if partnerss:
                    part = partnerss[0]
                    today_date = datetime.date.today()
                    sales_all = LeadsCount.objects.all()
                    check = 0

                    for sale in sales_all:
                        if sale.date == today_date and sale.partner == part:
                            check = 1

                    if check == 0:
                        saless = LeadsCount.objects.create(
                            lead_count=0, date=today_date, partner=part)
                        saless.save()

                    sale_today = LeadsCount.objects.get(
                        date=today_date, partner=part)
                    get_sale_count = sale_today.lead_count
                    sale_today.lead_count = get_sale_count+1
                    sale_today.save()
                    email = EmailMessage(
                        subject, body, emaill, ["contact@homebaba.ca",part.email],
                        reply_to=[email]
                    )
                    email.send(fail_silently=False)
                else:
                    email = EmailMessage(
                        subject, body, emaill, to=["contact@homebaba.ca"],
                        reply_to=[email]
                    )
                    email.send(fail_silently=False)
                return HttpResponse("Sucess")
            else:
                email = EmailMessage(
                    subject, body, emaill, ["contact@homebaba.ca"],
                    reply_to=[email], headers=headers
                )
                email.send(fail_silently=False)
                return HttpResponse("Sucess")
        else:
            email = EmailMessage(
                subject, body, emaill, ["contact@homebaba.ca"],
                reply_to=[email], headers=headers
            )
            email.send(fail_silently=False)
            return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")
    

@api_view(['GET'])
def slugify_all_news(request):
    developers = News.objects.all()
    for news in developers:
        news.slug = slugify(news.news_title)
        news.save()
    return Response({"message": "done"})


class TrackingEventListCreateView(generics.ListCreateAPIView):
    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer

class TrackingEventRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer