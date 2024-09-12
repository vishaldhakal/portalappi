from django.db import models

class Customer(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Visitor(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class Pageview(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=200)
    referrer = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor.id} - {self.url}"

class FormSubmission(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    form_id = models.CharField(max_length=50)
    form_action = models.URLField()
    form_method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor.id} - {self.form_id}"

class FormField(models.Model):
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    value = models.TextField()

    def __str__(self):
        return f"{self.form_submission.id} - {self.name}"