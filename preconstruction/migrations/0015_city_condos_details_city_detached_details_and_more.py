# Generated by Django 5.0.7 on 2024-10-01 08:23

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0014_delete_trackingevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='condos_details',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='detached_details',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='semi_detached_details',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
        migrations.AddField(
            model_name='city',
            name='townhomes_details',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='details',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
        migrations.AlterField(
            model_name='preconstruction',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True),
        ),
    ]