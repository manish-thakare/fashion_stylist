import os
import django

import sys
# print(sys.path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from myapp.models import Items

# Retrieve all items from the database
items = Items.objects.all()

# Loop through each item and convert the price attribute to float
for item in items:
    try:
        item.price = float(item.price)
        item.save()
    except ValueError:
        print(f"Error converting price for item {item.name}")
