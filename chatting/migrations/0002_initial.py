# Generated by Django 3.2.5 on 2021-07-09 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatting.thread'),
        ),
    ]
