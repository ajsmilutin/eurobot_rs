# Generated by Django 3.2.10 on 2021-12-26 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0012_auto_20211226_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eliminationgame',
            name='games_finished',
        ),
    ]
