# Generated by Django 2.2.4 on 2022-05-15 16:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220515_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 16, 10, 9, 787441, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 16, 10, 9, 784441, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='post_feedback',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 5, 15, 16, 10, 9, 786441, tzinfo=utc), verbose_name='Posted Date'),
        ),
        migrations.AlterField(
            model_name='post_feedback',
            name='like_post',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post_feedback',
            name='report_post',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]