# Generated by Django 3.2.6 on 2021-09-20 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Review',
            new_name='review',
        ),
    ]
