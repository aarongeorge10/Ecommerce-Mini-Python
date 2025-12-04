from django.db import models

# Create your models here.
class img_up(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    image = models.ImageField(null=True,blank=True,upload_to="images/")


class User_reg(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phonenumber = models.IntegerField(null=True)
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200,null=True)

class Cart(models.Model):
    user = models.ForeignKey(User_reg, on_delete=models.CASCADE)
    product = models.ForeignKey(img_up, on_delete=models.CASCADE)   # your product model name
    quantity = models.PositiveIntegerField(default=1)
