# Generated by Django 3.0.5 on 2020-05-02 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtdb', '0006_auto_20200502_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='facebook',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='gym',
            name='instagram',
            field=models.URLField(default=''),
        ),
    ]
