from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    brand = models.CharField(max_length=10)
    type = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="itemimages/", default='', blank=True)
    likes = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return f"{self.id}-{self.name}"

class Outfits(models.Model):
    id = models.AutoField(primary_key=True)
    upper_path = models.CharField(max_length=100)
    lower_path = models.CharField(max_length=100)
    foot_path = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    score = models.FloatField(default=0.0)
    items = models.ManyToManyField(Items)
    like = models.BooleanField(default = False)
    
    



