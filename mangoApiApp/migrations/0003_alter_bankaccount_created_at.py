# Generated by Django 4.1.7 on 2023-02-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangoApiApp', '0002_bankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='created_at',
            field=models.IntegerField(default=1677165266),
        ),
    ]
