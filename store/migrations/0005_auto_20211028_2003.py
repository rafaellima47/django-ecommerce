# Generated by Django 3.2.6 on 2021-10-28 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_avg_rate_product_avarage_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='avarage_rate',
        ),
        migrations.AddField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=1),
        ),
    ]
