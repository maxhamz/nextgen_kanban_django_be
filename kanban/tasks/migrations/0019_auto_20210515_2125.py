# Generated by Django 3.1.7 on 2021-05-15 14:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import enumfields.fields
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_auto_20210515_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 17, 14, 25, 32, 467427, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=enumfields.fields.EnumField(default='CRT', enum=tasks.models.TaskStatus, max_length=3),
        ),
    ]