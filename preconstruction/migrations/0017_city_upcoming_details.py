# Generated by Django 3.1.6 on 2024-10-06 09:18

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0016_auto_20241006_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='upcoming_details',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
    ]
