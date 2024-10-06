from django.db import migrations
from django.utils.text import slugify
from django.db.models import SlugField

def generate_unique_slug(apps, name, slug_field='slug'):
    Developer = apps.get_model('preconstruction', 'Developer')
    slug = slugify(name)
    original_slug = slug
    counter = 1
    while Developer.objects.filter(**{slug_field: slug}).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug

def generate_slugs(apps, schema_editor):
    Developer = apps.get_model('preconstruction', 'Developer')
    for developer in Developer.objects.all():
        developer.slug = generate_unique_slug(apps, developer.name)
        developer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0014_delete_trackingevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='slug',
            field=SlugField(max_length=255, unique=True, null=True),
        ),
        migrations.RunPython(generate_slugs),
    ]
