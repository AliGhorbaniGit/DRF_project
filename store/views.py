from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, SendPrivateEmailToCustomerPermission, CustomDjangoModelPermissions
from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, OrderItem
from .serializers import ProductSerializer , CategorySerializer, CommentSerializer, CartSerilizer, CartItemSerializer,CustomerSerializer, OrderSerializer,AddCartItemSerializer,UpdateCartItemSerializer,OrderCreateSerializer, OrderUpdateSerializer, OrderForAdminSerializer
from .paginations import DefaultPagination
from .signals import order_created



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['category','title','slug',]
    ordering_fields = ['name', 'unit_price', 'inventory']
    filterset_class = ProductFilter
    search_fields = ['title',]

    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    

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
            return Response({'error': 'There is some products relating this category. Please remove them first.'}, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        if self.request.user.is_staff:
            return Comment.objects.filter(product_id=product_pk).all()
        return Comment.objects.filter(product_id=product_pk, status='a').all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs.get('product_pk'),'user_id':self.request.user.id}
    
    def get_permissions(self):
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            try:
                comment = Comment.objects.get(pk=self.kwargs.get('pk'))
            except Comment.DoesNotExist:
                return [IsAdminUser()]

            if not self.request.user == Comment.objects.get(pk=self.kwargs.get('pk')).user_id:
                return [IsAdminUser()]
            # return [IsAuthenticated()]

        if self.request.method in ['POST']:    
            return [IsAuthenticated()]

        return [IsAuthenticated()]

class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    queryset = Cart.objects.prefetch_related(Prefetch(
        'items',
        queryset=CartItem.objects.select_related('product')
    )).all()
    serializer_class = CartSerilizer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer



class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        return Response(f'Sending email to customer {pk=}')



class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product'),
            )
        ).select_related('customer__user').all()

        user = self.request.user

        if user.is_staff:
            return queryset
        return queryset.filter(customer__user_id = user.id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer

        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        
        if self.request.user.is_staff:
            return OrderForAdminSerializer

        return OrderSerializer

    def create(self, request, *args, **kwargs):
         create_order_serializer = OrderCreateSerializer(
            data=request.data,
            context={'user_id': self.request.user.id},
        )
        
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()

        order_created.send_robust(self.__class__, order=created_order)

        serializer = OrderSerializer(created_order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance:
            # Disabling POST method by removing 'create' action from allowed actions
            self.allowed_methods['POST'].remove('create')
