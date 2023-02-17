# Generated by Django 4.1.6 on 2023-02-17 14:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=48)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]