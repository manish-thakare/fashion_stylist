from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upper_fav_colors = models.JSONField(default=list)
    lower_fav_colors = models.JSONField(default=list)
    item_time = models.DateTimeField(null=True)
    outfit_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    pattern=models.CharField(max_length=100)
    color = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    brand = models.CharField(max_length=10)
    type = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="itemimages/", default='', blank=True)
    like = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.id}-{self.name}"

class Outfits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    upper_id = models.IntegerField(null=True)
    lower_id = models.IntegerField(null=True)
    foot_id = models.IntegerField(null=True)
    type = models.CharField(max_length=100)
    score = models.FloatField(default=0.0)
    items = models.ManyToManyField(Items)
    like = models.BooleanField(default=False)
