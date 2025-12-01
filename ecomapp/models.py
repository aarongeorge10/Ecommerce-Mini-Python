from django.db import models

# Create your models here.
class img_up(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True,upload_to="images/")


class user(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phonenumber = models.IntegerField(null=True)
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200,null=True)


