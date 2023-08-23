from django.urls import path
from . import views
from rest_framework_nested import routers





router= routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('collection', views.CollectionViewSet)
router.register('cart', views.CartViewSet)







product_router= routers.NestedDefaultRouter(router, 'product', lookup= 'product')
product_router.register('reviews', views.ReviewViewSet, basename='product_reviews')

urlpatterns= router.urls  + product_router.urls 