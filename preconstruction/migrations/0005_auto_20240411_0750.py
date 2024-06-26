# Generated by Django 3.1.6 on 2024-04-11 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preconstruction', '0004_auto_20230927_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preconstruction',
            options={'ordering': ('-last_updated',)},
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image', models.FileField(blank=True, upload_to='')),
                ('partner_type', models.CharField(choices=[('Brokerage', 'Brokerage'), ('Real Estate Agent', 'Real Estate Agent'), ('Real Estate Salesperson', 'Real Estate Salesperson')], default='Real Estate Agent', max_length=500)),
                ('brokerage_name', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=500, unique=True)),
                ('cities', models.ManyToManyField(blank=True, to='preconstruction.City')),
            ],
        ),
        migrations.CreateModel(
            name='LeadsCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lead_count', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='preconstruction.partner')),
            ],
        ),
    ]
