from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store3.filters import ProductFilter
from store3.pagination import DefaultPagination
from . models import Cart, Product, Collection, OrderItem,  Review
from . serializers import  CartSerializer, ProductSerializer , CollectionSerializer, ReviewSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework import mixins
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin


# Create your views here.





   







class ProductViewSet(ModelViewSet):
   queryset= Product.objects.all()
   serializer_class= ProductSerializer
   filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
   filterset_class= ProductFilter
   search_fields= ['title', 'description']
   ordering_fields= [ 'last_update', 'unit_price']
   pagination_class =DefaultPagination


   queryset=Product.objects.all()
   Serializer_class=ProductSerializer


   
   def get_serializer_context(self):
      return {'request' : self.request}
   

   

   def delete(self, request,id):
      product=get_object_or_404(Product, pk=id)
      if product.cartitems.count()> 0:
            return Response({'error': 'Product cannot be fdeleted because it is associated with the carts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      product.delete() 
      return Response(status=status.HTTP_204_NO_CONTENT)
   
   def destroy(self, request, *args, **kwargs):
      if Product.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with the carts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      return super.destroy(self, request,*args, **kwargs)
   






      

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method=='GET':
     queryset = Product.objects.select_related('collection').all()
     serializer= ProductSerializer(queryset, many=True, context={'request': request})
     return Response(serializer.data)
    elif request.method=='POST':
      serializer= ProductSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
     
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    




@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
        try:
         product = get_object_or_404(Product, pk=id )
        except Product.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method=='GET':
         serializer = ProductSerializer(product)
         return Response(serializer.data) 

        elif request.method =='PUT':
         serializer=ProductSerializer(product, data=request.data)
         serializer.is_valid(raise_exception=True) 
         serializer.save()
         return Response(serializer.data)
        
        elif request.method== 'DELETE':
           if product.cartitems.count()> 0:
            return Response({'error': 'Product cannot be deleted because it is associated with the carts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
           product.delete() 
           return Response(status=status.HTTP_204_NO_CONTENT)
 




class CollectionViewSet(ModelViewSet):
       queryset = Collection.objects.annotate(product_count=Count('product')).all()
       serializer_class= CollectionSerializer


       queryset=Product.objects.all()
       Serializer_class=CollectionSerializer


def delete(self, request,id):
      collection=get_object_or_404(Collection, pk=id)
      if collection.cartitems.count()> 0:
            return Response({'error': 'Product cannot be fdeleted because it is associated with the carts'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
      collection.delete() 
      return Response(status=status.HTTP_204_NO_CONTENT)

def get_serializer_context(self):
      return {'request' : self.request}









@api_view(['GET', 'POST'])
def collection_List(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(product_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
        try:
         collection = get_object_or_404(Collection.objects.annotate(product_count=Count('product')), pk=id )
        except Collection.DoesNotExist:
           return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method=='GET':
         serializer = CollectionSerializer(collection)
         return Response(serializer.data) 

        elif request.method =='PUT':
         serializer=CollectionSerializer(Collection, data=request.data)
         serializer.is_valid(raise_exception=True) 
         serializer.save()
         return Response(serializer.data)
        
        elif request.method== 'DELETE':
           if Collection.product.all().count()> 0:
            return Response({'error': 'Collection cannot be deleted because it is associated with the product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
           collection.delete() 
           return Response(status=status.HTTP_204_NO_CONTENT)
    






class ListModelMixin:

 def list(self, request, *args, **kwargs):
    queryset=self.filter_query(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
       serializer = self.get_serializer(page, many=True)
       return self.get_paginated_response(serializer.data)
    
    serializer= self.get_serializer(queryset, many=True)
    return Response(serializer.data)
 

 class CreateModelMixin:
   
   def create(self, request, *args, **kwargs):
     serializer= self.get_serializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     self.perfom_create(serializer)
     headers = self.get_success_headers(serializer.data)
     return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   def perfom_create(self, serializer):
     serializer.save()


 class DestroyModelMixin:
   
   def destroy(self, request, *args, **kwargs):
     instance= self.get_object()
     self.perfom_destroy(instance)
     return Response(status=status.HTTP_204_NO_CONTENT)
   
   def perfom_destroy(self, instance):
     instance.save()




class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin):
   def get (self, request, *args, **kwargs):
     return self.list(request, *args, **kwargs)
    

   def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)





class ListProductMixin(mixins.ListModelMixin, generics.GenericAPIView):
     

     queryset=Product.objects.all()
     Serializer_class=ProductSerializer


def get(self, request, *args, **kwargs):
      return self.get(request, *args, **kwargs)





class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin):
    def get (self, request, *args, **kwargs):
     return self.list(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)





class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin):

   def get(self, request,*args, **kwargs):
      return self.retrieve(request,*args, **kwargs)
   
   def put(self, request,*args, **kwargs):
      return self.update(request,*args, **kwargs)
   
   def patch(self, request,*args, **kwargs):
      return self.partial_update(request,*args, **kwargs)
   
   def delete(self, request,*args, **kwargs):
      return self.destroy(request,*args, **kwargs)


         




class ReviewViewSet(ModelViewSet):
   serializer_class = ReviewSerializer

   def get_queryset(self):
      return Review.objects.filter(product_id=self.kwargs['product_pk'])

   def get_serializer_context(self):
      return {'product_id': self.kwargs['product_pk']}
   





class CartViewSet(CreateModelMixin,GenericViewSet):
   queryset= Cart.objects.all()
   serializer_class= CartSerializer