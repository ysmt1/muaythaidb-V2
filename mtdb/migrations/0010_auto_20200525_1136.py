# Generated by Django 3.0.5 on 2020-05-25 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtdb', '0009_auto_20200525_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='session_type',
            field=models.CharField(choices=[('group', 'Group'), ('private', 'Private')], default=None, max_length=200),
        ),
    ]
