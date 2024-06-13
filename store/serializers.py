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


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product','quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try :
            cart_item = CartItem.objects.get(cart_id=cart_id, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)


        self.instance = cart_item
        return cart_item



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


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
        read_only_fields = ['user',]


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'status', 'datetime_created'] 
        read_only_fields = ['customer', 'status', 'datetime_created']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        cart = Cart.objects.filter(id=cart_id)
        if not cart.exists():
            raise serializers.ValidationError('There is no cart with this cart id!')

        if cart.count() == 0 :
            raise serializers.ValidationError('Your cart is empty. Please add some products to it first!')

        return cart_id

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']



class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email']


class OrderForAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = OrderCustomerSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'datetime_created', 'items']
