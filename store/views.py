from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet


from .models import Product, Category, Comment, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer , CategorySerializer, CommentSerializer, CartSerilizer, CartItemSerializer,CustomerSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def destroy(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        count = product.order_items.count()
        if count > 0 :
            return Response({'error': f'there is {count} order item related to this product please delete theme first'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




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

