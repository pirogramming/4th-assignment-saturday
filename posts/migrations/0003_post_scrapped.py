# Generated by Django 2.2.5 on 2019-10-05 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20191005_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='scrapped',
            field=models.IntegerField(default=0),
        ),
    ]
