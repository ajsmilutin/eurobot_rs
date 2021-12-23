# Generated by Django 3.2.10 on 2021-12-23 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0006_alter_round_tournament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='opponent_color',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player_color',
        ),
        migrations.AlterField(
            model_name='game',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rounds', to='tournaments.round'),
        ),
    ]
