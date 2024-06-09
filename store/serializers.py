from decimal import Decimal
from django.utils.text import slugify

from rest_framework import serializers

from .models import Product, Category, Comment, Cart, CartItem, Customer, Order, Order


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250, source='title')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    unit_price_after_tax = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name','slug', 'price','unit_price_after_tax', 'category', 'inventory', 'description']
        read_only_fields = ['slug',]

    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)

    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError('mroduct title length should be more that 5 vharacters')
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.title)
        product.save()
        return product

class CategorySerializer(serializers.ModelSerializer):
    # num_of_products = serializers.SerializerMethodField()
    num_of_products = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'description', 'top_product', 'num_of_products' ]

    # def get_num_of_products(self, category):
    #     return category.products.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user' ,'product', 'body', 'datetime_created',  'status'   ]

        read_only_fields  = ['user', 'product', 'datetime_created', 'status']
    

    def create(self, validated_data):
        product_id = self.context['product_pk']
        user_id = self.context['user_id']
        return Comment.objects.create(product_id=product_id,user_id=user_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','item_total']

    def ge_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerilizer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','items','total_price']
        read_only_fields = ['id',]

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])





class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'phone_number', 'birth_date'] 


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'status', 'datetime_created'] 

