# Generated by Django 3.2.10 on 2021-12-23 00:12

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0007_auto_20211223_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='round',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rounds', to='tournaments.round'),
        ),
    ]
