from rest_framework import serializers
from store3.models import  Product, Collection, Review, Cart
from decimal import Decimal




class CollectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Collection
        fields= ['id', 'title']

        title= serializers.IntegerField(read_only=True)
    
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= ['id', 'title', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    
    price_with_tax= serializers.SerializerMethodField(method_name='calculate_tax')
    
    

    def calculate_tax(self, product:Product):
        return product.unit_price*Decimal(1.1)
   

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model= Review
        fields= ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)




class CartSerializer(serializers.ModelSerializer):  
   id=serializers.UUIDField(read_only=True)
   class Meta:
        model=Cart
        fields= ['id']