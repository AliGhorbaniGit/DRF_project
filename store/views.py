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




class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()



class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerilizer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

