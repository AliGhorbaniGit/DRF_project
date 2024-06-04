from rest_framework import serializers

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','unit_price','description','slug','category','discounts','inventory','datetime_created','datetime_modified',]


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

