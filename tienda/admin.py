# tienda/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario, Producto, Categoria, Pedido, DetallePedido, Carrito, Favorito

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False

class UserAdminCustom(UserAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'precio', 'stock', 'categoria', 'activo']
    list_filter = ['tipo', 'categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'total', 'estado', 'forma_pago']
    list_filter = ['estado', 'forma_pago', 'fecha_pedido']
    search_fields = ['usuario__username', 'domicilio']
    readonly_fields = ['fecha_pedido']

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    readonly_fields = ['subtotal']
    extra = 0

class PedidoAdminWithDetails(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'total', 'estado']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha_pedido']

# Reregistrar User admin
admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)

# Registrar otros modelos
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Carrito)
admin.site.register(Favorito)