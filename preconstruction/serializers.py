from rest_framework import serializers
from .models import Developer, City, PreConstruction, PreConstructionImage, PreConstructionFloorPlan, Event, News, Favourite
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


class CitySerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']


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
    city = CitySerializer()
    developer = DeveloperSerializer()

    class Meta:
        model = PreConstruction
        fields = '__all__'
        ordering = ['last_updated']


class PreConstructionSerializerSmall(serializers.ModelSerializer):
    image = PreConstructionImageSerializer(many=True, read_only=True)
    city = CitySerializerSmall()

    class Meta:
        model = PreConstruction
        fields = '__all__'
        ordering = ['last_updated']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        ordering = ['event_date']


class NewsSerializer(serializers.ModelSerializer):
    city = CitySerializer()

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
