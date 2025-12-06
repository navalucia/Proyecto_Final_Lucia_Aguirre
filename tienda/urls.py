# tienda/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # **PRIMERO LAS NUEVAS URLs CON SUBCATEGORÍAS (MÁS ESPECÍFICAS)**
    path('productos/cremas/', views.productos_cremas, name='productos_cremas'),
    path('productos/cremas/<str:subcategoria>/', views.productos_cremas, name='productos_cremas_subcategoria'),
    
    path('productos/limpiadores/', views.productos_limpiadores, name='productos_limpiadores'),
    path('productos/limpiadores/<str:subcategoria>/', views.productos_limpiadores, name='productos_limpiadores_subcategoria'),
    
    path('productos/cuidado-solar/', views.productos_cuidado_solar, name='productos_cuidado_solar'),
    path('productos/cuidado-solar/<str:subcategoria>/', views.productos_cuidado_solar, name='productos_cuidado_solar_subcategoria'),
    
    path('productos/maquillaje/', views.productos_maquillaje, name='productos_maquillaje'),
    path('productos/maquillaje/<str:subcategoria>/', views.productos_maquillaje, name='productos_maquillaje_subcategoria'),
    
    path('productos/mascarillas/', views.productos_mascarillas, name='productos_mascarillas'),
    path('productos/mascarillas/<str:subcategoria>/', views.productos_mascarillas, name='productos_mascarillas_subcategoria'),
    
    # **LUEGO LA URL ANTIGUA (MÁS GENÉRICA - para compatibilidad)**
    path('productos/<str:tipo>/', views.productos_por_tipo, name='productos_tipo'),
    
    # Carrito y favoritos
    path('carrito/', views.carrito_view, name='carrito'),
    path('favoritos/', views.favoritos_view, name='favoritos'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar-carrito/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('agregar-favorito/<int:producto_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('eliminar-favorito/<int:favorito_id>/', views.eliminar_favorito, name='eliminar_favorito'),
    
    # URLs AJAX para carrito
    path('carrito/actualizar/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar-item/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    # Pedidos de usuario
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedido/cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
    
    # Panel de administración
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-productos/', views.admin_productos, name='admin_productos'),
    path('admin-editar-producto/<int:producto_id>/', views.admin_editar_producto, name='admin_editar_producto'),
    path('admin-eliminar-producto/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    path('admin-pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin-detalle-pedido/<int:pedido_id>/', views.admin_detalle_pedido, name='admin_detalle_pedido'),
    path('admin-usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-cambiar-password/', views.admin_cambiar_password, name='admin_cambiar_password'),
    
    # **NUEVA URL PARA TOGGLE DESTACADO**
    path('admin-toggle-destacado/<int:producto_id>/', views.toggle_destacado, name='toggle_destacado'),
    
    # Nuevas URLs para gestión de pedidos
    path('admin-pedidos/actualizar-estado/<int:pedido_id>/', views.admin_actualizar_estado_pedido, name='admin_actualizar_estado_pedido'),
    path('admin-pedidos/cancelar/<int:pedido_id>/', views.admin_cancelar_pedido, name='admin_cancelar_pedido'),
]