# Generated by Django 2.2.4 on 2020-10-09 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindle', '0005_star'),
    ]

    operations = [
        migrations.AddField(
            model_name='star',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
