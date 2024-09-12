import json
import base64
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Customer, Visitor, Pageview, FormSubmission, FormField

@ensure_csrf_cookie
@require_http_methods(["POST"])
def config(request):
    data = json.loads(request.body)
    customer = get_object_or_404(Customer, id=data.get('customerId'))
    
    config = {
        "widgetConfig": True,
        "captureForms": True,
        "customerId": customer.id,
    }
    
    return JsonResponse(config)

@ensure_csrf_cookie
@require_http_methods(["POST"])
def pages(request):
    data = json.loads(request.body)
    customer = get_object_or_404(Customer, id=data.get('customerId'))
    visitor, _ = Visitor.objects.get_or_create(id=data.get('visitorId'), customer=customer)
    
    Pageview.objects.create(
        visitor=visitor,
        url=data.get('url'),
        title=data.get('title'),
        referrer=data.get('referrer')
    )
    
    return JsonResponse({"status": "success"})

@ensure_csrf_cookie
@require_http_methods(["POST"])
def identify(request):
    data = json.loads(request.body)
    customer = get_object_or_404(Customer, id=data.get('customerId'))
    visitor = get_object_or_404(Visitor, id=data.get('visitorId'), customer=customer)
    
    visitor.email = data.get('email')
    visitor.save()
    
    return JsonResponse({"status": "success"})

@ensure_csrf_cookie
@require_http_methods(["POST"])
def form(request):
    data = json.loads(request.body)
    customer = get_object_or_404(Customer, id=data.get('customerId'))
    visitor = get_object_or_404(Visitor, id=data.get('visitorId'), customer=customer)
    
    form_data = data.get('form', {})
    form_submission = FormSubmission.objects.create(
        visitor=visitor,
        form_id=form_data.get('id'),
        form_action=form_data.get('action'),
        form_method=form_data.get('method')
    )
    
    for field in form_data.get('fields', []):
        FormField.objects.create(
            form_submission=form_submission,
            name=field.get('name'),
            value=field.get('value')
        )
    
    return JsonResponse({"status": "success"})

@ensure_csrf_cookie
def pixel(request):
    # Serve a 1x1 transparent GIF
    return HttpResponse(base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'), content_type='image/gif')