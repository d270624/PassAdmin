# Generated by Django 2.1.4 on 2018-12-13 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20181208_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersGroup',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='分组名称')),
                ('hostgroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Group', verbose_name='分组')),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='user_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Group', verbose_name='分组'),
        ),
    ]
