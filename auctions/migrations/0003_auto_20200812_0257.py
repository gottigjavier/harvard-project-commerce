# Generated by Django 3.1 on 2020-08-12 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200811_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(default='all', max_length=30),
        ),
    ]
