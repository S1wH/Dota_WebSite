# Generated by Django 4.1.7 on 2023-04-10 09:08

from django.db import migrations, models
import django.db.models.deletion

ID_KEY = (
    "id",
    models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID")
)


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ID_KEY,
                ("name", models.CharField(max_length=30)),
                ("nickname", models.CharField(max_length=15)),
                ("age", models.IntegerField()),
                ("birthday", models.DateField()),
                ("country", models.CharField(max_length=20)),
                ("photo", models.ImageField(upload_to="players_photos")),
                ("biography", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ID_KEY,
                ("win_matches", models.IntegerField(default=0)),
                ("lose_matches", models.IntegerField(default=0)),
                ("draw_matches", models.IntegerField(default=0)),
                ("prize", models.IntegerField(default=0)),
                ("name", models.CharField(max_length=20)),
                ("country", models.CharField(max_length=20)),
                ("establish_date", models.DateField()),
                ("logo", models.ImageField(upload_to="teams_logos")),
                ("biography", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CareerPeriod",
            fields=[
                ID_KEY,
                ("win_matches", models.IntegerField(default=0)),
                ("lose_matches", models.IntegerField(default=0)),
                ("draw_matches", models.IntegerField(default=0)),
                ("prize", models.IntegerField(default=0)),
                ("role", models.CharField(max_length=15)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player_career",
                        to="teams_and_players.player",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_career",
                        to="teams_and_players.team",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
