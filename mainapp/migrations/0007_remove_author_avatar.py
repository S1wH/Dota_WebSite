# Generated by Django 4.1.7 on 2023-03-06 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_author_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='avatar',
        ),
    ]
