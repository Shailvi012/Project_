from django.db import models

# Create your models here.
class Register(models.Model):
    Name = models.CharField(max_length=20)
    Email = models.EmailField()
    Password = models.CharField(max_length=15)
    Mobile_number = models.IntegerField()
    boolean = models.BooleanField(default=False)

class Category(models.Model):
    cat_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.cat_name

class Product(models.Model):
    cat_name= models.ForeignKey(Category,on_delete=models.CASCADE)
    pro_name= models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.TextField(max_length=100)
    image = models.ImageField(upload_to="proImg")

class Contact(models.Model):
    Name = models.CharField(max_length=20)
    Number = models.IntegerField()
    Message = models.TextField(max_length=50)
    
class Slider(models.Model):
    image = models.ImageField(upload_to= "sliderImg")
    
class Cart(models.Model):
    User = models.ForeignKey(Register,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quntity = models.IntegerField()

class Order(models.Model):
    User = models.ForeignKey(Register,on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete= models.CASCADE)
    Email = models.EmailField()
    Mobile = models.IntegerField()
    Address = models.TextField()
    Country = models.CharField(max_length=20) 
