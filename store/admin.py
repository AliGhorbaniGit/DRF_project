from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.db.models import Count

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
    list_display = ('title','unit_price','description','slug','product_category',
                    'inventory','inventory_status','num_of_comments','datetime_created',
                    'datetime_modified', )
    list_display_order = 10
    list_editable = ['unit_price', 'inventory', ]
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['title',]
    prepopulated_fields = {
        'slug': ['title', ]
    }
    autocomplete_fields = ['category', 'discounts']
    authenticate_fiels = ['title']

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .prefetch_related('comments').annotate(
                comments_count=Count('comments'),
            )

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

    @admin.display(ordering='category__title')
    def product_category(self, product):
        return product.category.title

    @admin.display(description='# comments', ordering='comments_count')
    def num_of_comments(self, product):
        url = (
            reverse('admin:store_comment_changelist') 
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
        

@admin.register(models.Discount)
class DiscounttAdmin(admin.ModelAdmin):
    list_display = ['title','discount','description']
    search_fields = ['title',]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','description','top_product']
    search_fields = ['title']



@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','body','datetime_created','status']
    list_editable = ['status',]
    list_per_page = 10
    autocomplete_fields = ['product', ]
    authenticate_fiels = ['body']
    actions = ['make_status_to_approve',]
    list_select_related = ['product']
    search_fields = ['product__title']


    


    @admin.action(description='make status to approve')
    def make_status_to_approve(self, request, queryset):
        update_status = queryset.update(status='a')
        self.message_user(request, f'{update_status} comment Approved')




@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','birth_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']



@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer','province','city','street']


class OrderItemsInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product', 'quantity', 'unit_price']
    extra = 1
    min_num = 1
    autocomplete_fields = ['product']
    


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','status','num_of_items', 'datetime_created', ]
    list_editable = ['status',]
    list_per_page = 10
    ordering = ['-datetime_created']
    inlines = [OrderItemsInline,]
    list_select_related = ['customer',]
    search_fields = ['id','customer__user__username','customer__user__first_name',
    'customer__user__last_name','customer__user__email','customer__phone_number']
    autocomplete_fields = ['customer', ]
    list_filter = ['datetime_created', 'status', 'customer']

    def get_queryset(self, request):
        return super()\
            .get_queryset(request)\
            .prefetch_related('items')\
            .annotate(
                items_count=Count('items')
            )

    def num_of_items(self, order):
        return order.items_count


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','unit_price']
    # search_fields = ['product__title']



@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','created_at']



@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']

