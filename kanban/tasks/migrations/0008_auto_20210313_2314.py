# Generated by Django 3.1.7 on 2021-03-13 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20210313_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 15, 23, 14, 1, 667424)),
        ),
    ]
