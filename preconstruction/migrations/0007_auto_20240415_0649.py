# Generated by Django 3.1.6 on 2024-04-15 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0006_domains'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='contact_email',
            field=models.CharField(max_length=500),
        ),
    ]
