from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact, ConfirmEmailToken, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, \
    Order, OrderItem


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact

    list_display = ('user', 'city', 'phone')


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'key',)


@admin.register(Shop)
class ContactAdmin(admin.ModelAdmin):
    model = Shop


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    model = ProductInfo
    list_display = ('product', 'model', 'shop')


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    model = Parameter


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    model = ProductParameter


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    models = Order
    list_display = ('user', 'dt')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    models = OrderItem
    list_display = ('order', 'product_info')
