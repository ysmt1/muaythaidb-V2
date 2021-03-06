# Generated by Django 3.0.5 on 2020-05-25 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtdb', '0007_auto_20200502_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='session_type',
            field=models.CharField(choices=[('group', 'Group'), ('private', 'Private')], default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='gym',
            name='facebook',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='gym',
            name='instagram',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='gym',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
    ]
