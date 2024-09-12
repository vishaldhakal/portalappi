from django.contrib import admin
from .models import Customer, Visitor, Pageview, FormSubmission, FormField


admin.site.register(Customer)
admin.site.register(Visitor)
admin.site.register(Pageview)
admin.site.register(FormSubmission)
admin.site.register(FormField)
