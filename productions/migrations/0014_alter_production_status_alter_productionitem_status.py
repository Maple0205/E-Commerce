# Generated by Django 5.0.2 on 2024-04-22 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productions', '0013_alter_production_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pulished'), (2, 'UnPublished'), (3, 'OutOfStock')], default=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='productionitem',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pulished'), (2, 'UnPublished'), (3, 'OutOfStock')], default=2, verbose_name='Status'),
        ),
    ]