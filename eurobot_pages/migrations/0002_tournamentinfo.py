# Generated by Django 3.2.10 on 2021-12-21 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0005_game_round'),
        ('eurobot_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentInfo',
            fields=[
                ('richtextpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='eurobot_pages.richtextpage')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.tournament')),
            ],
            options={
                'abstract': False,
            },
            bases=('eurobot_pages.richtextpage',),
        ),
    ]
