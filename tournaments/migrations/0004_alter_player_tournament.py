# Generated by Django 3.2.10 on 2021-12-21 17:36

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_player_tournament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='tournament',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournaments.tournament'),
        ),
    ]