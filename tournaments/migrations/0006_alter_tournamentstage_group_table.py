# Generated by Django 4.1.7 on 2023-07-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0005_tournamentstage_group_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tournamentstage",
            name="group_table",
            field=models.JSONField(blank=True, default={}, null=True),
        ),
    ]