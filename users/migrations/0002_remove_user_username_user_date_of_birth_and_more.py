# Generated by Django 5.1.1 on 2024-09-15 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=datetime.datetime(2024, 9, 15, 16, 52, 37, 257705, tzinfo=datetime.timezone.utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='online_shop/user/images/'),
        ),
    ]
