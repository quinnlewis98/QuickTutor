# Generated by Django 3.0.3 on 2020-02-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20200223_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tutor_mode',
            field=models.BooleanField(),
        ),
    ]
