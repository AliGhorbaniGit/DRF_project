from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from uuid import uuid4
from django.utils.text import slugify


class Discount(models.Model):
    """ this is the discount model """

    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    discount = models.FloatField(verbose_name=_('discount'))
    description = models.CharField(max_length=255, verbose_name=_('description'))

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'



class Category(models.Model):
    """ this is the category model """

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    title = models.CharField(max_length=255, verbose_name='title')
    description = models.CharField(max_length=500, blank=True, verbose_name='description')
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+', verbose_name='top product')

    def __str__(self):
        return self.title


class Product(models.Model):
    """ THIS IS THE PRODUCT MODEL  """

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    title = models.CharField(max_length=250, verbose_name='title')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('unit price'))
    # image = models.ImageField(upload_to='image/products_image', verbose_name=_('image'))
    description = models.TextField(max_length=1000, verbose_name=_('description'), blank=True)
    slug = models.SlugField(verbose_name=_('slug'))

    category = models.ForeignKey(Category,on_delete=models.PROTECT, related_name='products', verbose_name=_('category'))
    discounts = models.ManyToManyField(Discount, blank=True, verbose_name=_('discounts'))

    inventory = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_("inventory"))
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True, blank=True)


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    """ this is comments model """
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', )

    body = models.TextField(max_length=1000,verbose_name='body')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING, verbose_name='status')

    # objects = CommentManger()
    # approved = ApprovedCommentManager()



class Customer(models.Model):
    """ this is the customer model """
    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('user'))
    # image = models.ImageField(upload_to='image/products_image', verbose_name=_('image'))
    phone_number = models.IntegerField(null=True,blank=True, verbose_name=_("phone_number"), )
    birth_date = models.DateField(null=True,blank=True,verbose_name=_('birth date'))

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Address(models.Model):
    """ this is the address model for customer """

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=250, verbose_name=_('province'))
    city = models.CharField(max_length=250, verbose_name=_('city'))
    street = models.CharField(max_length=250, verbose_name=_('street'))


class Order(models.Model):
    """ this is the order model """

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    ORDER_STATUS_PAID = 'P'
    ORDER_STATUS_UNPAID = 'U'
    ORDER_STATUS_CANCELED = 'C'

    ORDER_STATUS = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]


    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders', verbose_name=_('customer'))
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID, verbose_name=_('status'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created time'))

    def __str__(self):
        return f'Order id={self.id}'





class OrderItem(models.Model):
    """ this is the order Items model """

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name=_('product'))
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta:
        unique_together = [['order', 'product']]


class Cart(models.Model):
    """ this is the cart model """

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    id = models.UUIDField(primary_key=True, default=uuid4,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))


class CartItem(models.Model):
    """ this is the cart items model """

    class Meta:
        verbose_name = _('cart items')
        verbose_name_plural = _('carts items')

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(_('quantity'))
    

