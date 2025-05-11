from rest_framework import serializers
from .models import Developer, City, PreConstruction, PreConstructionImage, PreConstructionFloorPlan, Event, News, Favourite,Partner,Domains
from accounts.serializers import AgentSerializer


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'
        ordering = ['name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        ordering = ['name']

class CitySerializerMain(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['condos_details','townhomes_details','detached_details','upcoming_details']
        ordering = ['name']

class CitySerializerCondos(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['details','townhomes_details','detached_details','upcoming_details']
        ordering = ['name']

class CitySerializerDetached(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['condos_details','townhomes_details','details','upcoming_details']
        ordering = ['name']

class CitySerializerTownhomes(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['condos_details','details','detached_details','upcoming_details']
        ordering = ['name']

class CitySerializerUpcoming(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['condos_details','townhomes_details','detached_details','details']
        ordering = ['name']

class CitySerializerSmallest(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['slug']


class CitySerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']

class PartnerSerializer(serializers.ModelSerializer):
    cities = CitySerializerSmall(many=True)
    class Meta:
        fields = '__all__'
        model = Partner
        depth = 1

class PreConstructionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionImage
        fields = ('id', 'image')
        ordering = ['id']


class PreConstructionFloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreConstructionFloorPlan
        fields = ('id', 'floorplan')
        ordering = ['id']


class PreConstructionSerializer(serializers.ModelSerializer):
    image = PreConstructionImageSerializer(many=True, read_only=True)
    floorplan = PreConstructionFloorPlanSerializer(many=True, read_only=True)
    city = CitySerializerSmall()
    developer = DeveloperSerializer()

    class Meta:
        model = PreConstruction
        fields = '__all__'
        ordering = ['last_updated']


class DeveloperSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['name']

class PreConstructionSerializerSmallVsmall(serializers.ModelSerializer):
    city = CitySerializerSmall()
    class Meta:
        model = PreConstruction
        fields = ['id', 'slug', 'project_name', 'city', 'status','project_type','project_address','occupancy','last_updated',"is_featured"]
        ordering = ["is_featured",'last_updated']

class PreConstructionSerializerSmall(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    city = CitySerializerSmall()
    developer = DeveloperSerializerSmall()

    class Meta:
        model = PreConstruction
        fields = ['id', 'slug', 'project_name', 'city', 'developer', 'image','price_starting_from','price_to','is_featured','status','project_type','project_address','occupancy','last_updated']
        ordering = ["is_featured",'last_updated']
    
    def get_image(self, obj):
        image = PreConstructionImage.objects.filter(preconstruction=obj).first()
        serializer = PreConstructionImageSerializer(image)
        return serializer.data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        ordering = ['event_date']


class CitySerializerSmallestNews(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']

class NewsSerializerSmall(serializers.ModelSerializer):
    city = CitySerializerSmallestNews()
    class Meta:
        model = News
        fields = ['id', 'news_title', 'slug', 'city', 'date_of_upload', 'last_updated','news_thumbnail','news_link']
        ordering = ['date_of_upload']

class NewsSerializer(serializers.ModelSerializer):
    city = CitySerializerSmallestNews()

    class Meta:
        model = News
        fields = '__all__'
        ordering = ['date_of_upload']


class FavouriteSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()
    preconstruction = PreConstructionSerializer()

    class Meta:
        model = Favourite
        fields = '__all__'

class PreConstructionSearchSerializer(serializers.ModelSerializer):

    city = CitySerializerSmallest()
    class Meta:
        model = PreConstruction
        fields = ['id','slug','project_name','city', 'project_type']
        ordering = ['last_updated']


class CitySerializerSmallSearch(serializers.ModelSerializer):
    preconstructions = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ['id', 'name', 'slug','preconstructions']

    def get_preconstructions(self, obj):
        preconstructions = PreConstruction.objects.filter(city=obj)
        serializer = PreConstructionSearchSerializer(preconstructions, many=True)
        return serializer.data

class DomainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domains
        fields = '__all__'
        ordering = ['id']
