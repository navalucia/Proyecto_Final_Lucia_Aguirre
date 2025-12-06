from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from decimal import Decimal
import json

from .models import Producto, Carrito, Favorito, Pedido, DetallePedido, Categoria, AdminPersonalizado
from .forms import RegistroForm, ProductoForm, PedidoForm

# Función para verificar si es administrador personalizado
def es_administrador_personalizado(user):
    if not user.is_authenticated:
        return False
    try:
        return AdminPersonalizado.objects.filter(usuario=user, activo=True).exists()
    except:
        return False

# Decorador personalizado para acceso al admin - SOLO ADMINISTRADORES
def admin_access_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and es_administrador_personalizado(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "No tienes permisos para acceder al administrador")
            return redirect('index')
    return wrapper

def calcular_total_carrito(usuario):
    items_carrito = Carrito.objects.filter(usuario=usuario)
    total = Decimal('0.00')
    for item in items_carrito:
        total += item.producto.precio * item.cantidad
    return total

def index(request):
    # **ACTUALIZADO: Productos destacados (seleccionados manualmente)**
    productos_destacados = Producto.objects.filter(
        destacado=True, 
        activo=True, 
        stock__gt=0
    )[:8]
    
    # Obtener productos por categoría
    productos_limpiadores = Producto.objects.filter(tipo='limpiadores', activo=True, stock__gt=0)[:4]
    productos_cremas = Producto.objects.filter(tipo='cremas', activo=True, stock__gt=0)[:4]
    productos_maquillaje = Producto.objects.filter(tipo='maquillaje', activo=True, stock__gt=0)[:4]
    
    context = {
        'productos_destacados': productos_destacados,
        'productos_limpiadores': productos_limpiadores,
        'productos_cremas': productos_cremas,
        'productos_maquillaje': productos_maquillaje,
    }
    return render(request, 'index.html', context)

def productos_por_tipo(request, tipo):
    if request.user.is_authenticated and es_administrador_personalizado(request.user):
        return redirect('admin_dashboard')
    
    productos = Producto.objects.filter(tipo=tipo, activo=True)
    titulo = dict(Producto.TIPO_PRODUCTO).get(tipo, 'Productos')
    return render(request, f'productos/{tipo}.html', {
        'productos': productos,
        'titulo': titulo,
        'tipo_producto': tipo
    })

# **NUEVAS VISTAS CON SUBCATEGORÍAS**
def productos_cremas(request, subcategoria=None):
    productos = Producto.objects.filter(
        tipo='cremas', 
        activo=True
    )
    
    titulo = "Cremas"
    subcategorias_cremas = [
        {'value': 'hidratante', 'text': 'Crema Hidratante'},
        {'value': 'anti_edad', 'text': 'Crema Anti-Edad'},
        {'value': 'contorno_ojos', 'text': 'Contorno de Ojos'},
        {'value': 'noche', 'text': 'Crema de Noche'},
        {'value': 'dia', 'text': 'Crema de Día'},
    ]
    
    if subcategoria:
        productos = productos.filter(subcategoria=subcategoria)
        # Encontrar el nombre de la subcategoria
        for sub in subcategorias_cremas:
            if sub['value'] == subcategoria:
                titulo = f"Cremas - {sub['text']}"
                break
    
    context = {
        'productos': productos,
        'titulo': titulo,
        'subcategorias': subcategorias_cremas,
        'tipo_actual': 'cremas'
    }
    return render(request, 'productos_con_subcategorias.html', context)

def productos_limpiadores(request, subcategoria=None):
    productos = Producto.objects.filter(
        tipo='limpiadores', 
        activo=True
    )
    
    titulo = "Limpiadores Faciales"
    subcategorias_limpiadores = [
        {'value': 'gel', 'text': 'Gel Limpiador'},
        {'value': 'espuma', 'text': 'Espuma Limpiadora'},
        {'value': 'aceite', 'text': 'Aceite Limpiador'},
        {'value': 'agua_micelar', 'text': 'Agua Micelar'},
    ]
    
    if subcategoria:
        productos = productos.filter(subcategoria=subcategoria)
        for sub in subcategorias_limpiadores:
            if sub['value'] == subcategoria:
                titulo = f"Limpiadores - {sub['text']}"
                break
    
    context = {
        'productos': productos,
        'titulo': titulo,
        'subcategorias': subcategorias_limpiadores,
        'tipo_actual': 'limpiadores'
    }
    return render(request, 'productos_con_subcategorias.html', context)

def productos_cuidado_solar(request, subcategoria=None):
    productos = Producto.objects.filter(
        tipo='cuidado_solar', 
        activo=True
    )
    
    titulo = "Cuidado Solar"
    subcategorias_solar = [
        {'value': 'protector_facial', 'text': 'Protector Solar Facial'},
        {'value': 'protector_corporal', 'text': 'Protector Solar Corporal'},
        {'value': 'protector_mineral', 'text': 'Protector Mineral'},
        {'value': 'after_sun', 'text': 'After Sun'},
    ]
    
    if subcategoria:
        productos = productos.filter(subcategoria=subcategoria)
        for sub in subcategorias_solar:
            if sub['value'] == subcategoria:
                titulo = f"Cuidado Solar - {sub['text']}"
                break
    
    context = {
        'productos': productos,
        'titulo': titulo,
        'subcategorias': subcategorias_solar,
        'tipo_actual': 'cuidado_solar'
    }
    return render(request, 'productos_con_subcategorias.html', context)

def productos_maquillaje(request, subcategoria=None):
    productos = Producto.objects.filter(
        tipo='maquillaje', 
        activo=True
    )
    
    titulo = "Maquillaje"
    subcategorias_maquillaje = [
        {'value': 'base', 'text': 'Base de Maquillaje'},
        {'value': 'labial', 'text': 'Labiales'},
        {'value': 'sombras', 'text': 'Sombras de Ojos'},
        {'value': 'rubor', 'text': 'Rubor'},
    ]
    
    if subcategoria:
        productos = productos.filter(subcategoria=subcategoria)
        for sub in subcategorias_maquillaje:
            if sub['value'] == subcategoria:
                titulo = f"Maquillaje - {sub['text']}"
                break
    
    context = {
        'productos': productos,
        'titulo': titulo,
        'subcategorias': subcategorias_maquillaje,
        'tipo_actual': 'maquillaje'
    }
    return render(request, 'productos_con_subcategorias.html', context)

def productos_mascarillas(request, subcategoria=None):
    productos = Producto.objects.filter(
        tipo='mascarillas', 
        activo=True
    )
    
    titulo = "Mascarillas"
    subcategorias_mascarillas = [
        {'value': 'arcilla', 'text': 'Mascarilla de Arcilla'},
        {'value': 'hidratante', 'text': 'Mascarilla Hidratante'},
        {'value': 'sheet_mask', 'text': 'Sheet Mask'},
        {'value': 'purificante', 'text': 'Mascarilla Purificante'},
    ]
    
    if subcategoria:
        productos = productos.filter(subcategoria=subcategoria)
        for sub in subcategorias_mascarillas:
            if sub['value'] == subcategoria:
                titulo = f"Mascarillas - {sub['text']}"
                break
    
    context = {
        'productos': productos,
        'titulo': titulo,
        'subcategorias': subcategorias_mascarillas,
        'tipo_actual': 'mascarillas'
    }
    return render(request, 'productos_con_subcategorias.html', context)

# **NUEVA VISTA: Toggle para productos destacados**
@login_required
def toggle_destacado(request, producto_id):
    if not es_administrador_personalizado(request.user):
        return HttpResponseForbidden("No tienes permisos para esta acción")
    
    producto = get_object_or_404(Producto, id=producto_id)
    producto.destacado = not producto.destacado
    producto.save()
    
    messages.success(request, f'Producto {"marcado como destacado" if producto.destacado else "quitado de destacados"}')
    return redirect('admin_productos')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if es_administrador_personalizado(user):
                messages.success(request, f'¡Bienvenido Administrador {user.username}!')
                return redirect('admin_dashboard')
            else:
                messages.success(request, f'¡Bienvenido/a {user.username}!')
                return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def registro_view(request):
    if request.user.is_authenticated and es_administrador_personalizado(request.user):
        messages.error(request, 'Los administradores no pueden crear cuentas de usuario')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('index')
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('index')

# Vistas de usuario normal
@login_required
def carrito_view(request):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden("Los administradores no pueden realizar compras")
    
    items_carrito = Carrito.objects.filter(usuario=request.user)
    total = calcular_total_carrito(request.user)
    iva = total * Decimal('0.16')
    total_con_iva = total + iva
    
    if request.method == 'POST':
        forma_pago = request.POST.get('forma_pago')
        direccion_calle = request.POST.get('direccion_calle')
        # ... (resto de campos de dirección)
        
        if items_carrito.exists() and forma_pago and direccion_calle:
            # Simplificado para el ejemplo, mantener tu lógica de creación de pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                forma_pago=forma_pago,
                total=total_con_iva,
                direccion_calle=direccion_calle
                # Añadir el resto de campos según tu modelo
            )
            
            for item in items_carrito:
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                    subtotal=item.producto.precio * item.cantidad
                )
                item.producto.stock -= item.cantidad
                item.producto.save()
            
            items_carrito.delete()
            messages.success(request, '¡Compra realizada exitosamente!')
            return redirect('index')
        else:
            messages.error(request, 'Error al procesar la compra')
    
    return render(request, 'carrito.html', {
        'items_carrito': items_carrito,
        'total': total,
        'iva': iva,
        'total_con_iva': total_con_iva
    })

@login_required
def favoritos_view(request):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden("Los administradores no pueden usar favoritos")
    favoritos = Favorito.objects.filter(usuario=request.user)
    return render(request, 'favoritos.html', {'favoritos': favoritos})

@login_required
def agregar_carrito(request, producto_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden("Los administradores no pueden agregar productos")
    
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        carrito_item, created = Carrito.objects.get_or_create(
            usuario=request.user,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        if not created:
            carrito_item.cantidad += cantidad
            carrito_item.save()
        messages.success(request, f'{producto.nombre} agregado al carrito')
        return redirect('carrito')
    return redirect('index')

@login_required
def eliminar_carrito(request, item_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    item = get_object_or_404(Carrito, id=item_id, usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('carrito')

@login_required
def actualizar_carrito(request):
    if es_administrador_personalizado(request.user):
        return JsonResponse({'success': False})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Carrito, id=data.get('item_id'), usuario=request.user)
            cantidad = int(data.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

@login_required
def eliminar_del_carrito(request):
    if es_administrador_personalizado(request.user):
        return JsonResponse({'success': False})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = get_object_or_404(Carrito, id=data.get('item_id'), usuario=request.user)
            item.delete()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

@login_required
def agregar_favorito(request, producto_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        Favorito.objects.get_or_create(usuario=request.user, producto=producto)
        messages.success(request, 'Agregado a favoritos')
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def eliminar_favorito(request, favorito_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    favorito = get_object_or_404(Favorito, id=favorito_id, usuario=request.user)
    favorito.delete()
    messages.success(request, 'Eliminado de favoritos')
    return redirect('favoritos')

@login_required
def mis_pedidos(request):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'mis_pedidos.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'usuarios/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles})

@login_required
def cancelar_pedido(request, pedido_id):
    if es_administrador_personalizado(request.user):
        return HttpResponseForbidden()
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    if pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save()
        messages.success(request, 'Pedido cancelado exitosamente')
    return redirect('mis_pedidos')

# --- VISTAS ADMINISTRADOR ---

@login_required
@admin_access_required
def admin_dashboard(request):
    usuarios_normales = User.objects.filter(adminpersonalizado__isnull=True).count()
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    productos_bajo_stock = Producto.objects.filter(stock__lt=10).count()
    pedidos_recientes = Pedido.objects.order_by('-fecha_pedido')[:5]
    
    return render(request, 'admin/dashboard.html', {
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'total_usuarios': usuarios_normales,
        'productos_bajo_stock': productos_bajo_stock,
        'pedidos_recientes': pedidos_recientes
    })

@login_required
@admin_access_required
def admin_cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada exitosamente')
            return redirect('admin_dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'admin/cambiar_password.html', {'form': form})

@login_required
@admin_access_required
def admin_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Guardar la subcategoría si se proporciona
            subcategoria = request.POST.get('opcion_especifica')
            if subcategoria:
                producto.subcategoria = subcategoria
            producto.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('admin_productos')
    else:
        form = ProductoForm()
    
    return render(request, 'admin/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'form': form
    })

@login_required
@admin_access_required
def admin_editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto_editado = form.save(commit=False)
            # Actualizar la subcategoría si se proporciona
            subcategoria = request.POST.get('opcion_especifica')
            if subcategoria:
                producto_editado.subcategoria = subcategoria
            producto_editado.save()
            messages.success(request, 'Producto actualizado')
            return redirect('admin_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin/editar_producto.html', {'form': form, 'producto': producto})

@login_required
@admin_access_required
def admin_eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Si el método es POST (usuario confirmó en la página nueva), borramos
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('admin_productos')
    
    # Si el método es GET (click en el enlace), mostramos la página de confirmación
    return render(request, 'admin/eliminar_producto.html', {'producto': producto})

@login_required
@admin_access_required
def admin_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'admin/pedidos.html', {'pedidos': pedidos})

@login_required
@admin_access_required
def admin_detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado actualizado')
            return redirect('admin_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'admin/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles, 'form': form})

@login_required
@admin_access_required
def admin_usuarios(request):
    usuarios_normales = User.objects.filter(adminpersonalizado__isnull=True)
    return render(request, 'admin/usuarios.html', {'usuarios': usuarios_normales})

# NUEVAS VISTAS PARA GESTIÓN DE PEDIDOS
@login_required
@admin_access_required
def admin_actualizar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        
        # Usar ESTADO_PEDIDO del modelo (que es el nombre correcto)
        estados_validos = [choice[0] for choice in Pedido.ESTADO_PEDIDO]
        
        # Verificar que el estado sea válido
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Estado del pedido #{pedido_id} actualizado a {nuevo_estado}')
        else:
            messages.error(request, 'Estado no válido')
        return redirect('admin_pedidos')

@login_required
@admin_access_required
def admin_cancelar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        if pedido.estado != 'cancelado':
            pedido.estado = 'cancelado'
            pedido.save()
            messages.success(request, f'Pedido #{pedido_id} cancelado exitosamente')
        else:
            messages.warning(request, f'El pedido #{pedido_id} ya está cancelado')
        return redirect('admin_pedidos')

def carrito_context(request):
    if request.user.is_authenticated and not es_administrador_personalizado(request.user):
        cantidad_carrito = Carrito.objects.filter(usuario=request.user).count()
        cantidad_favoritos = Favorito.objects.filter(usuario=request.user).count()
    else:
        cantidad_carrito = 0
        cantidad_favoritos = 0
    return {
        'cantidad_carrito': cantidad_carrito,
        'cantidad_favoritos': cantidad_favoritos,
        'es_administrador': es_administrador_personalizado(request.user) if request.user.is_authenticated else False
    }