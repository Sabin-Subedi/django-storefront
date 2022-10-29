from email.policy import default
from enum import unique
from http.client import PAYMENT_REQUIRED
from itertools import product
from secrets import choice
from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name="+")
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE ='B'
    MEMBERSHIP_SILVER ='S'
    MEMBERSHIP_GOLD ='G'
    
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    
    
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'    
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'PENDING'),
        (PAYMENT_STATUS_COMPLETED, 'COMPLETED'),
        (PAYMENT_STATUS_FAILED, 'FAILED'),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
    
class Address(models.Model):
    city= models.CharField(max_length=255)
    street= models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    



