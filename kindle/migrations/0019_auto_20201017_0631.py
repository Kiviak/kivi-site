# Generated by Django 2.2.4 on 2020-10-17 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kindle', '0018_ebookreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebookreview',
            name='ebookreviews',
            field=models.ManyToManyField(to='kindle.Ebookreview'),
        ),
    ]