# Generated by Django 2.1.4 on 2018-12-13 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_auto_20181213_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersgroup',
            old_name='hostgroup',
            new_name='Group',
        ),
    ]
