# Generated by Django 4.1.7 on 2023-03-12 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='news_images'),
        ),
    ]
