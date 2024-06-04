from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer 



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category','title','slug',]
    search_fields = ['title',]

    permission_classes = [IsAdminOrReadOnly]
