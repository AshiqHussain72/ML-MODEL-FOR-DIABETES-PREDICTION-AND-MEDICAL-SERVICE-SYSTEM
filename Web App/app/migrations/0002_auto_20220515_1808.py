# Generated by Django 2.2.4 on 2022-05-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_detail',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='register_detail',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
