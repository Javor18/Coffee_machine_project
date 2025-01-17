# Generated by Django 4.1.7 on 2023-03-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee_machine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffemachine',
            name='price_without_profit',
        ),
        migrations.RemoveField(
            model_name='coffemachine',
            name='profit_percCent',
        ),
        migrations.AlterField(
            model_name='coffemachine',
            name='price_with_profit',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='coffemachine',
            name='productName',
            field=models.CharField(max_length=100),
        ),
    ]
