# Generated by Django 4.2.6 on 2024-02-10 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0011_alter_items_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="outfits",
            name="items",
            field=models.ManyToManyField(to="myapp.items"),
        ),
    ]