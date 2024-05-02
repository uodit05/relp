# Generated by Django 5.0.4 on 2024-05-02 16:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busslogic', '0002_remove_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]