# Generated by Django 3.2.10 on 2021-12-21 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_auto_20211221_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournaments.tournament'),
        ),
    ]
