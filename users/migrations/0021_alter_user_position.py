# Generated by Django 5.0.2 on 2024-04-29 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_position_alter_user_recipient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='position'),
        ),
    ]
