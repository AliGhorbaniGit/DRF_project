from rest_framework import serializers

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','unit_price','description','slug','category','discounts','inventory','datetime_created','datetime_modified',]
