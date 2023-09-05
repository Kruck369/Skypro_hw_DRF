# Generated by Django 4.2.4 on 2023-09-05 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payed_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='оплаченный курс'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payed_lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.lesson', verbose_name='оплаченный урок'),
        ),
    ]
