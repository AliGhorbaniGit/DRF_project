from django.contrib import admin

from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','unit_price','description','slug','category',
                    'inventory','datetime_created','datetime_modified')


@admin.register(models.Discount)
class DiscounttAdmin(admin.ModelAdmin):
    list_display = ['discount','description']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','description','top_product']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','body','datetime_created','status']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','birth_date']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer','province','city','street']


class OrderItemsInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','status','datetime_created']
    inlines = [OrderItemsInline,]


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','unit_price']



@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']



@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']

