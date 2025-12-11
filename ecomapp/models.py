from django.db import models

# Create your models here.
class img_up(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True,blank=True,upload_to="images/")
    description = models.TextField(blank=True, null=True, max_length=200)
    trailer = models.FileField(upload_to="trailers/", blank=True, null=True)
    


class User_reg(models.Model):
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phonenumber = models.IntegerField(null=True)
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200,null=True)

class Cart(models.Model):
    user = models.ForeignKey(User_reg, on_delete=models.CASCADE)
    product = models.ForeignKey(img_up, on_delete=models.CASCADE)   
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User_reg, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(img_up, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)