# Generated by Django 2.1.4 on 2019-02-28 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0023_auto_20190226_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('result', models.TextField()),
            ],
        ),
    ]
