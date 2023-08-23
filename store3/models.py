from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib import admin

from core.models import User
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title 
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)
    inventory= models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection, related_name='product', on_delete=models.PROTECT)
    promotion=models.ManyToManyField(Promotion)

class Costumer(models.Model):
    MEMBER_BRONZE = 'B'
    MEMBER_SILVER = 'S'
    MEMBER_GOLD = 'G'
    MEMBERSHIP_CHOICES=[
        (MEMBER_BRONZE, 'Bronze'),
        (MEMBER_SILVER, 'Silver'),
        (MEMBER_GOLD, 'Gold'),

    ]
    
    phone=models.CharField(max_length=255)
    birth_date=models.DateTimeField(null=True)    
    membership=models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBER_BRONZE)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)


    def __str__(self) :
        return f'{self.user.first_name} {self.user.last_name}'
    
    
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    
    class Meta:
        ordering=['user__first_name', 'user__last_name']

    permissions= [
        ('cancel Customer', 'Can cancel Customer')
    ]

class Address (models.Model):
    street = models.CharField(max_length=255)
    city= models.CharField(max_length=255)  
    customer = models.ForeignKey(Costumer, on_delete=models.CASCADE)  

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'p'
    PAYMENT_STATUS_COMPLETE = 'C' 
    PAYMENT_STATUS_FAILED = 'F' 
    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]    

    placed_at= models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    amount=models.DecimalField(max_digits=6, decimal_places=2)
    quantity=models.PositiveSmallIntegerField()
    costumer= models.ForeignKey(Costumer, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.first_name



class OrderItem(models.Model):
    Order=models.ForeignKey(Order, on_delete=models.PROTECT)
    costumer=models.ForeignKey(Costumer, on_delete=models.PROTECT)
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)
    quantity=models.PositiveSmallIntegerField()






class Cart(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True)





class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()







    



class Review(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name= models.CharField(max_length=255)
    description=models.TextField()
    date= models.DateField(auto_now_add=True)


