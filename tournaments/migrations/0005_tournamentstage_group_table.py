# Generated by Django 4.1.7 on 2023-07-01 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tournaments", "0004_tournamentstage_teams_alter_tournament_teams"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournamentstage",
            name="group_table",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
