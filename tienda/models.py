from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class AdminPersonalizado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Admin: {self.usuario.username}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('maquillaje', 'Maquillaje'),
        ('cuidado_solar', 'Cuidado Solar'),
        ('mascarillas', 'Mascarillas'),
        ('cremas', 'Cremas'),
        ('limpiadores', 'Limpiadores Faciales'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='productos/')
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    
    # **NUEVOS CAMPOS AGREGADOS**
    destacado = models.BooleanField(default=False)
    subcategoria = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def precio_con_iva(self):
        return self.precio * 1.16

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Usuario: {self.usuario.username}"

class Pedido(models.Model):
    FORMA_PAGO = [
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('paypal', 'PayPal'),
        ('transferencia', 'Transferencia Bancaria'),
    ]
    
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # ELIMINAR el campo domicilio y usar solo los campos detallados
    # domicilio = models.TextField()  # ← ELIMINAR ESTA LÍNEA
    
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='pendiente')
    direccion_calle = models.CharField(max_length=255)
    direccion_numero_exterior = models.CharField(max_length=10)
    direccion_numero_interior = models.CharField(max_length=10, blank=True, null=True)
    direccion_colonia = models.CharField(max_length=100)
    direccion_codigo_postal = models.CharField(max_length=5)
    direccion_ciudad = models.CharField(max_length=100)
    direccion_estado = models.CharField(max_length=50)
    direccion_referencias = models.TextField(blank=True, null=True)
    
    # Campos para pago con tarjeta (guardar solo los últimos 4 dígitos por seguridad)
    tarjeta_ultimos_digitos = models.CharField(max_length=4, blank=True, null=True)
    tarjeta_tipo = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
    @property
    def domicilio(self):
        """Propiedad para compatibilidad con código existente"""
        return f"{self.direccion_calle} #{self.direccion_numero_exterior}" + \
               (f" Int. {self.direccion_numero_interior}" if self.direccion_numero_interior else "") + \
               f", {self.direccion_colonia}, {self.direccion_ciudad}, {self.direccion_estado}, C.P. {self.direccion_codigo_postal}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'producto')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'producto')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"