# Generated by Django 3.2.4 on 2021-06-23 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
