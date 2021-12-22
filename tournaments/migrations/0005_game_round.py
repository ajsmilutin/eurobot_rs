# Generated by Django 3.2.10 on 2021-12-21 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_alter_player_tournament'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('round_date', models.DateTimeField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='tournaments.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_color', models.CharField(choices=[('W', 'White'), ('B', 'Black')], default='W', max_length=1)),
                ('player_score', models.PositiveIntegerField(default=0)),
                ('player_dummy', models.BooleanField(default=False)),
                ('opponent_score', models.PositiveIntegerField(default=0)),
                ('opponent_color', models.CharField(choices=[('W', 'White'), ('B', 'Black')], default='B', max_length=1)),
                ('opponent_dummy', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('finished', 'Finished')], default='planned', max_length=10)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_b', to='tournaments.player')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_a', to='tournaments.player')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.round')),
            ],
        ),
    ]