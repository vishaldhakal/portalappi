# Generated by Django 3.1.6 on 2024-10-06 08:06

from django.db import migrations, models
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0015_developer_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='condos_details',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='detached_details',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='townhomes_details',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='slug',
            field=models.SlugField(blank=True, max_length=520, unique=True),
        ),
    ]