from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import base64
from .models import Customer, Visitor, Pageview, FormSubmission, FormField
from .serializers import ConfigSerializer, PageviewSerializer, VisitorSerializer, FormSubmissionSerializer

class ConfigView(APIView):
    def post(self, request):
        customer = get_object_or_404(Customer, idd=1)
        config = {
            "widgetConfig": True,
            "captureForms": True,
            "customerId": customer.idd,
        }
        serializer = ConfigSerializer(data=config)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PageView(APIView):
    def post(self, request):
        customer = get_object_or_404(Customer, idd=1)
        visitor, _ = Visitor.objects.get_or_create(id=request.data.get('visitorId'), customer=customer)
        
        serializer = PageviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(visitor=visitor)
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IdentifyView(APIView):
    def post(self, request):
        customer = get_object_or_404(Customer, idd=1)
        visitor = get_object_or_404(Visitor, id=request.data.get('visitorId'), customer=customer)
        
        serializer = VisitorSerializer(visitor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FormView(APIView):
    def post(self, request):
        customer = get_object_or_404(Customer, idd=1)
        visitor = get_object_or_404(Visitor, id=request.data.get('visitorId'), customer=customer)
        
        serializer = FormSubmissionSerializer(data=request.data.get('form', {}))
        if serializer.is_valid():
            form_submission = serializer.save(visitor=visitor)
            
            for field in request.data.get('form', {}).get('fields', []):
                FormField.objects.create(
                    form_submission=form_submission,
                    name=field.get('name'),
                    value=field.get('value')
                )
            
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pixel(request):
    return HttpResponse(base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'), content_type='image/gif')