from decimal import Decimal
from rest_framework import serializers

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, Order


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250, source='title')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'price','unit_price_after_tax', 'category', 'inventory', 'description']
    
    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'description', 'top_product' ]



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user' ,'product', 'body', 'datetime_created',  'status'   ]



class CartSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','created_at']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','cart','product','quantity']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'phone_number', 'birth_date'] 


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'datetime_created'] 

