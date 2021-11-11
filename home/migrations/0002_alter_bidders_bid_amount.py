# Generated by Django 3.2.7 on 2021-11-04 18:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidders',
            name='bid_amount',
            field=models.FloatField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9]', 'Only numerics are allowed.')]),
        ),
    ]