# Generated by Django 4.1.5 on 2023-02-03 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatchlists', '0009_alter_episode_options_alter_season_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='imdb_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]