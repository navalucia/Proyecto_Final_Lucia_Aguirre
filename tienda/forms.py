from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Pedido, PerfilUsuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    telefono = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear el perfil de usuario sin dirección
            PerfilUsuario.objects.create(
                usuario=user,
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                telefono=self.cleaned_data['telefono'],
                direccion=""  # Dirección vacía, se pedirá en el pedido
            )
        return user

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'tipo', 'nombre', 'precio', 'stock', 'categoria',
            'foto', 'descripcion', 'activo', 'destacado'
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'forma_pago', 
            'direccion_calle', 
            'direccion_numero_exterior', 
            'direccion_numero_interior', 
            'direccion_colonia', 
            'direccion_codigo_postal', 
            'direccion_ciudad', 
            'direccion_estado', 
            'direccion_referencias',
            'estado'
        ]
        widgets = {
            'forma_pago': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'direccion_calle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle', 'required': True}),
            'direccion_numero_exterior': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número exterior', 'required': True}),
            'direccion_numero_interior': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número interior (opcional)'}),
            'direccion_colonia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia', 'required': True}),
            'direccion_codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal', 'required': True, 'maxlength': '5'}),
            'direccion_ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad', 'required': True}),
            'direccion_estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado', 'required': True}),
            'direccion_referencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Referencias adicionales (opcional)'}),
            'estado': forms.HiddenInput(),
        }