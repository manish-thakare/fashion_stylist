# Generated by Django 5.0.2 on 2024-03-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_items_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfits',
            name='foot_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='outfits',
            name='lower_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='outfits',
            name='upper_id',
            field=models.IntegerField(null=True),
        ),
    ]
