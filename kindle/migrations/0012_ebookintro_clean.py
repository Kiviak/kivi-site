# Generated by Django 2.2.4 on 2020-10-11 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kindle', '0011_ebookintro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ebookintro_clean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.TextField()),
                ('ebook', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kindle.Ebook')),
            ],
        ),
    ]
