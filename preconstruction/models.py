from django.db import models
from django_summernote.fields import SummernoteTextField
from accounts.models import Agent
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Developer(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=200, blank=True)
    website_link = models.TextField(blank=True)
    details = models.TextField()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=City)
def pre_save_slug(sender, instance, *args, **kwargs):
    base_slug = slugify(instance.name)
    unique_slug = base_slug
    num = 1
    while City.objects.filter(slug=unique_slug).exists():
        unique_slug = base_slug + "-" + str(num)
        num += 1
    instance.slug = unique_slug


class PreConstruction(models.Model):

    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Planning Phase", "Planning Phase"),
        ("Sold out", "Sold out")
    ]

    ASSIGNMENT_CHOICES = [
        ("Free", "Free"),
        ("Not Available", "Not Available"),
        ("Available With Fee", "Available With Fee")
    ]
    PROJECT_CHOICES = [
        ("Condo", "Condo"),
        ("Townhome", "Townhome"),
        ("Semi-Detached", "Semi-Detached"),
        ("Detached", "Detached"),
        ("NaN", "NaN"),
    ]

    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    builder_sales_email = models.CharField(max_length=500)
    builder_sales_phone = models.CharField(max_length=500)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    price_starting_from = models.FloatField(default=0)
    price_to = models.FloatField(default=0)
    project_type = models.CharField(
        max_length=500, choices=PROJECT_CHOICES, default="NaN")
    description = SummernoteTextField(blank=True)
    project_address = models.CharField(max_length=500)
    status = models.CharField(
        max_length=500, choices=STATUS_CHOICES, default="Upcoming")
    co_op_available = models.BooleanField(default=False)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.project_name + " [ " + self.city.name+" ] "

    class Meta:
        ordering = ('-date_of_upload',)


@receiver(pre_save, sender=PreConstruction)
def pre_save_slug(sender, instance, *args, **kwargs):
    base_slug = slugify(instance.project_name)
    unique_slug = base_slug
    num = 1
    while PreConstruction.objects.filter(slug=unique_slug).exists():
        unique_slug = base_slug + "-" + str(num)
        num += 1
    instance.slug = unique_slug


class PreConstructionImage(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name='image')
    image = models.FileField()

    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return "/media/no-image.webp"


class PreConstructionFloorPlan(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name='floorplan')
    floorplan = models.FileField()

    def __str__(self):
        return self.floorplan.url


class Event(models.Model):
    event_description = SummernoteTextField(blank=True)
    event_date = models.DateTimeField()
    event_link = models.CharField(max_length=2000, default="#")
    event_title = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.event_title


class News(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=1000)
    news_thumbnail = models.FileField(blank=True)
    news_description = SummernoteTextField(blank=True)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    news_link = models.CharField(max_length=2000, default="#")

    def __str__(self):
        return self.event_title


class Favourite(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="agent")
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="preconstruction")


class FavouriteNews(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="news_agent")
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="news")


class FavouriteEvent(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="event_agent")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event")
