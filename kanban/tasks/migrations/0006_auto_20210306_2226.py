# Generated by Django 3.1.7 on 2021-03-06 15:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210304_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 8, 22, 26, 30, 658146)),
        ),
    ]
