from rest_framework import serializers
from .models import Pageview, Visitor, FormSubmission

class ConfigSerializer(serializers.Serializer):
    widgetConfig = serializers.BooleanField()
    captureForms = serializers.BooleanField()
    customerId = serializers.IntegerField()

class PageviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pageview
        fields = ['url', 'title', 'referrer']

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['email']

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = ['form_id', 'form_action', 'form_method']