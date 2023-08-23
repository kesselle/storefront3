from django.shortcuts import render
from store3.models import Product, Order, Costumer
from django.db.models import Value, F, Func, Count
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
def say_hello(request):
     
          costumer= Costumer.objects.annotate(
                  full_name=Concat('first_name', Value(' '), 'last_name')
          )
          costumer= Costumer.objects.annotate(
                  Order_count=Count('order')
                  
                  )
          return render(request, 'hello.html', {'name': 'Kesselle', 'costumer': costumer})
    

