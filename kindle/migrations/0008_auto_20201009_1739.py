# Generated by Django 2.2.4 on 2020-10-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindle', '0007_ebookreal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebookreal',
            name='size',
            field=models.IntegerField(null=True),
        ),
    ]