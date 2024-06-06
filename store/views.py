from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from .models import Product, Category, Comment, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer , CategorySerializer, CommentSerializer, CartSerilizer, CartItemSerializer,CustomerSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['category','title','slug',]
    filterset_class = ProductFilter
    search_fields = ['title',]

    permission_classes = [IsAdminOrReadOnly]

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

    permission_classes = [IsAdminOrReadOnly, ]

    def destroy(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some products relating this category. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        



class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        return Comment.objects.filter(product_id=product_pk, status='a').all()
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs.get('product_pk'),'user_id':self.request.user.id}
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            # product_pk = self.kwargs.get('product_pk')
            # Comment = Comment.objects.get(pk=self.kwargs.get('pk'))
            if not self.request.user == Comment.objects.get(pk=self.kwargs.get('pk')).user_id:
                return [IsAdminUser()]
            return True
        if self.request.method in ['POST']:    
            return [IsAuthenticated()]

        return [IsAuthenticated()]

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

