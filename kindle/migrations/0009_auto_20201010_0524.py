# Generated by Django 2.2.4 on 2020-10-10 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindle', '0008_auto_20201009_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebookreal',
            name='size',
            field=models.BigIntegerField(null=True),
        ),
    ]
