from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_status', 'get_total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]
    fieldsets = (
        ('کاربر', {
            'fields': ('user',)
        }),
        ('وضعیت و مبلغ', {
            'fields': ('status', 'total_price')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'وضعیت'
    
    def get_total(self, obj):
        return f"{obj.total_price} تومان"
    get_total.short_description = 'مبلغ'