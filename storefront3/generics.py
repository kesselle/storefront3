from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Product, Collection
from . serializers import ProductSerializer , CollectionSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import mixins



class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin):
    def get (self, request, *args, **kwargs):
     return self.list(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)
    


