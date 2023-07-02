# Generated by Django 4.1.7 on 2023-06-29 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams_and_players", "0001_initial"),
        ("tournaments", "0003_alter_tournamentstage_stage"),
    ]

    operations = [
        migrations.AddField(
            model_name="tournamentstage",
            name="teams",
            field=models.ManyToManyField(
                related_name="tournaments_stages", to="teams_and_players.team"
            ),
        ),
        migrations.AlterField(
            model_name="tournament",
            name="teams",
            field=models.ManyToManyField(
                related_name="tournaments", to="teams_and_players.team"
            ),
        ),
    ]
