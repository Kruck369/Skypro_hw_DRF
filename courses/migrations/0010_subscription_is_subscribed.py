# Generated by Django 4.2.4 on 2023-09-12 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_subscribed',
            field=models.BooleanField(default=False, verbose_name='статус подписки'),
        ),
    ]