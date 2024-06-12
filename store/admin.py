from django.contrib import admin, messages

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_and_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
        
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_3_and_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','unit_price','description','slug','category',
                    'inventory','inventory_status','datetime_created','datetime_modified')
    list_display_order = 10
    list_editable = ['unit_price', 'inventory', 'category']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['title',]
    prepopulated_fields = {
        'slug': ['title', ]
    }

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} of products inventories cleared to zero.',
            messages.ERROR,
        )

    
    def inventory_status(self, product):
        if product.inventory <10:
            return 'low'
        if product.inventory > 50:
            return 'High'
        return 'Medium'













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

