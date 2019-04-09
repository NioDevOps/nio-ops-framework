# Generated by Django 2.1.7 on 2019-04-04 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfapp', '0004_auto_20190403_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepdefine',
            name='after_init',
            field=models.ManyToManyField(blank=True, default=[], related_name='after_init_hook', to='wfapp.Hook'),
        ),
        migrations.AddField(
            model_name='stepdefine',
            name='before_init',
            field=models.ManyToManyField(blank=True, default=[], related_name='before_init_hook', to='wfapp.Hook'),
        ),
    ]