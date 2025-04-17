from django.db import models
from tinymce.models import HTMLField
from accounts.models import Agent
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Developer(models.Model):
    image = models.FileField()
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=520, unique=True, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    website_link = models.TextField(blank=True)
    details = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(models.Model):
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    details = HTMLField(blank=True)
    condos_details = HTMLField(blank=True)
    townhomes_details = HTMLField(blank=True)
    detached_details = HTMLField(blank=True)
    upcoming_details = HTMLField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class PreConstruction(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Selling", "Selling"),
        ("Planning Phase", "Planning Phase"),
        ("Sold out", "Sold out"),
    ]

    ASSIGNMENT_CHOICES = [
        ("Free", "Free"),
        ("Not Available", "Not Available"),
        ("Available With Fee", "Available With Fee"),
    ]
    PROJECT_CHOICES = [
        ("Condo", "Condo"),
        ("Townhome", "Townhome"),
        ("Semi-Detached", "Semi-Detached"),
        ("Detached", "Detached"),
        ("NaN", "NaN"),
    ]
    is_featured = models.BooleanField(default=False)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    occupancy = models.CharField(max_length=500)
    no_of_units = models.CharField(max_length=500)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    slug = models.CharField(max_length=1000, unique=True)
    price_starting_from = models.FloatField(default=0)
    price_to = models.FloatField(default=0)
    project_type = models.CharField(
        max_length=500, choices=PROJECT_CHOICES, default="NaN"
    )
    description = HTMLField(blank=True)
    project_address = models.CharField(max_length=500)
    status = models.CharField(
        max_length=500, choices=STATUS_CHOICES, default="Upcoming"
    )
    co_op_available = models.BooleanField(default=False)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name + " [ " + self.city.name + " ] "

    class Meta:
        ordering = ("-is_featured","-last_updated",)


class PreConstructionImage(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="image"
    )
    image = models.FileField()

    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return "/media/no-image.webp"


class PreConstructionFloorPlan(models.Model):
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="floorplan"
    )
    floorplan = models.FileField()

    def __str__(self):
        return self.floorplan.url


class Event(models.Model):
    event_description = HTMLField(blank=True)
    event_date = models.DateTimeField()
    event_link = models.CharField(max_length=2000, default="#")
    event_title = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.event_title


class News(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    news_title = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000, blank=True)
    news_thumbnail = models.FileField(blank=True)
    news_description = HTMLField(blank=True)
    date_of_upload = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    news_link = models.CharField(max_length=2000, default="#")

    def __str__(self):
        return self.news_title


class Favourite(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="agent")
    preconstruction = models.ForeignKey(
        PreConstruction, on_delete=models.CASCADE, related_name="preconstruction"
    )


class FavouriteNews(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="news_agent"
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news")


class FavouriteEvent(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="event_agent"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")


class Partner(models.Model):
    TYPE_CHOICES = [
        ("Brokerage", "Brokerage"),
        ("Real Estate Agent", "Real Estate Agent"),
        ("Real Estate Salesperson", "Real Estate Salesperson"),
    ]

    name = models.CharField(max_length=500)
    image = models.FileField(blank=True)
    partner_type = models.CharField(
        max_length=500, choices=TYPE_CHOICES, default="Real Estate Agent"
    )
    brokerage_name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500, unique=True)
    cities = models.ManyToManyField(City, blank=True)

    def __str__(self):
        return str(self.name)


class LeadsCount(models.Model):
    lead_count = models.IntegerField(default=0)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_created=False, auto_now_add=False)

    def __str__(self):
        return str(self.lead_count)


class Domains(models.Model):
    domain = models.CharField(max_length=500)
    contact_email = models.CharField(max_length=500)

    def __str__(self):
        return str(self.domain)
