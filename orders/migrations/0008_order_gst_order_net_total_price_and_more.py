# Generated by Django 5.0.2 on 2024-04-23 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='net_total_price',
            field=models.FloatField(default=0, verbose_name='net_total_price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(verbose_name='total_price'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sum_price',
            field=models.FloatField(default=0),
        ),
    ]