# Generated by Django 5.0.2 on 2024-03-21 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update_time')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('sku', models.CharField(blank=True, max_length=100, unique=True, verbose_name='sku')),
                ('class_grade', models.CharField(blank=True, max_length=100, null=True, verbose_name='class_grade')),
                ('standard', models.CharField(blank=True, max_length=100, null=True, verbose_name='standard')),
                ('plating', models.CharField(blank=True, max_length=100, null=True, verbose_name='plating')),
                ('status', models.IntegerField(choices=[(1, 'Pulished'), (2, 'UnPublished')], default=2, verbose_name='Status')),
                ('single_item', models.BooleanField(default=True, verbose_name='single_item')),
                ('highest_price', models.FloatField(blank=True, null=True, verbose_name='highest_price')),
                ('lowest_price', models.FloatField(blank=True, null=True, verbose_name='lowest_price')),
            ],
            options={
                'verbose_name': 'productions',
                'db_table': 'productions',
            },
        ),
        migrations.CreateModel(
            name='ProductionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update_time')),
                ('is_delete', models.BooleanField(default=False, verbose_name='is_delete')),
                ('price', models.FloatField(verbose_name='price')),
                ('promotion_price', models.FloatField(blank=True, null=True, verbose_name='promotion_price')),
                ('sku', models.CharField(blank=True, max_length=100, unique=True, verbose_name='sku')),
                ('images', models.CharField(max_length=500, null=True, verbose_name='images')),
                ('size', models.CharField(blank=True, max_length=100, verbose_name='size')),
                ('status', models.IntegerField(choices=[(1, 'Pulished'), (2, 'UnPublished')], default=2, verbose_name='Status')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='productions.production')),
            ],
            options={
                'verbose_name': 'production_item',
                'db_table': 'production_item',
            },
        ),
    ]