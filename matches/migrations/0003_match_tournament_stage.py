# Generated by Django 4.1.7 on 2023-04-23 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
        ('matches', '0002_alter_match_format_alter_match_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='tournament_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournamentstage_matches', to='tournaments.tournamentstage'),
        ),
    ]
