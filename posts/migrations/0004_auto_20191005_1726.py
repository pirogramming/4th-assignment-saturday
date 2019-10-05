# Generated by Django 2.2.5 on 2019-10-05 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_scrapped'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['scrapped']},
        ),
        migrations.AlterField(
            model_name='post',
            name='scrapped',
            field=models.TextField(default=''),
        ),
    ]