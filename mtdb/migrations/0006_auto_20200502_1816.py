# Generated by Django 3.0.5 on 2020-05-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtdb', '0005_auto_20191223_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='website',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='training_length',
            field=models.IntegerField(default=0),
        ),
    ]
