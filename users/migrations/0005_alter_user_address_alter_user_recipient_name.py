# Generated by Django 5.0.2 on 2024-03-04 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_is_active_remove_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='', max_length=150, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='recipient_name',
            field=models.CharField(default='', max_length=150, verbose_name='recipient_name'),
        ),
    ]