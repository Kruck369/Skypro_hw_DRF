# Generated by Django 4.2.4 on 2023-09-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_subscription_is_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='стоимость'),
        ),
    ]
