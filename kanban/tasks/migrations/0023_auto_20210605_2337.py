# Generated by Django 3.1.7 on 2021-06-05 16:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_auto_20210605_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 7, 16, 37, 22, 781146, tzinfo=utc)),
        ),
    ]
