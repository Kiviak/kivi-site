# Generated by Django 2.2.4 on 2020-10-07 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kindle', '0004_auto_20201007_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kindle.Ebook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ebook')},
            },
        ),
    ]
