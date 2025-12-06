// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    inicializarDropdowns();
    inicializarModales();
    inicializarInteraccionesProductos();
    inicializarFormularios();
    inicializarAdmin();
});

// Dropdown menus
// Dropdown menus - ACTUALIZADO
function inicializarDropdowns() {
    function toggleDropdown() {
        const dropdown = document.getElementById('dropdownMenu');
        if (dropdown) {
            dropdown.classList.toggle('show');
        }
    }

    window.toggleDropdown = toggleDropdown;

    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        const dropdown = document.getElementById('dropdownMenu');
        const accountBtn = document.querySelector('.account-btn');
        
        if (dropdown && !e.target.matches('.account-btn') && !accountBtn.contains(e.target)) {
            dropdown.classList.remove('show');
        }
    });
} 

// Modales
function inicializarModales() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('show');
            }
        });
    });
}

// Interacciones con productos
function inicializarInteraccionesProductos() {
    const formsCarrito = document.querySelectorAll('form[action*="agregar-carrito"]');
    formsCarrito.forEach(form => {
        form.addEventListener('submit', function(e) {
            mostrarNotificacion('Producto agregado al carrito', 'success');
        });
    });
    
    const formsFavoritos = document.querySelectorAll('form[action*="agregar-favorito"]');
    formsFavoritos.forEach(form => {
        form.addEventListener('submit', function(e) {
            mostrarNotificacion('Producto agregado a favoritos', 'success');
        });
    });
    
    const tarjetasProducto = document.querySelectorAll('.card');
    tarjetasProducto.forEach(tarjeta => {
        tarjeta.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        tarjeta.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Formularios
function inicializarFormularios() {
    const formRegistro = document.querySelector('.register-form');
    if (formRegistro) {
        formRegistro.addEventListener('submit', function(e) {
            const password1 = document.getElementById('id_password1');
            const password2 = document.getElementById('id_password2');
            
            if (password1 && password2 && password1.value !== password2.value) {
                e.preventDefault();
                mostrarError('Las contraseñas no coinciden', password2);
            }
        });
    }
    
    const formLogin = document.querySelector('.login-form');
    if (formLogin) {
        formLogin.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (username && password && (!username.value || !password.value)) {
                e.preventDefault();
                mostrarError('Por favor completa todos los campos', username);
            }
        });
    }
}

// Admin
function inicializarAdmin() {
    if (!window.location.pathname.includes('admin')) return;
    
    // Búsqueda en tablas
    const tablas = document.querySelectorAll('.table');
    tablas.forEach(tabla => {
        const filas = tabla.querySelectorAll('tbody tr');
        const busqueda = document.createElement('input');
        busqueda.type = 'text';
        busqueda.placeholder = 'Buscar...';
        busqueda.className = 'form-control mb-3';
        busqueda.style.maxWidth = '300px';
        
        if (tabla.parentNode) {
            tabla.parentNode.insertBefore(busqueda, tabla);
        }
        
        busqueda.addEventListener('input', function() {
            const texto = this.value.toLowerCase();
            filas.forEach(fila => {
                const textoFila = fila.textContent.toLowerCase();
                fila.style.display = textoFila.includes(texto) ? '' : 'none';
            });
        });
    });
}

// Utilidades
function mostrarNotificacion(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${tipo}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
    `;
    toast.innerHTML = `
        ${mensaje}
        <button type="button" class="modal-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

function mostrarError(mensaje, elemento) {
    const errorPrevio = elemento.parentNode.querySelector('.error-mensaje');
    if (errorPrevio) {
        errorPrevio.remove();
    }
    
    const error = document.createElement('div');
    error.className = 'error-mensaje';
    error.style.cssText = 'color: #dc3545; font-size: 0.875rem; margin-top: 0.25rem;';
    error.textContent = mensaje;
    
    elemento.parentNode.appendChild(error);
    elemento.focus();
    
    elemento.style.borderColor = '#dc3545';
    setTimeout(() => {
        elemento.style.borderColor = '';
    }, 3000);
}

// Funciones globales para modales
window.abrirModalAgregar = function() {
    document.getElementById('modalAgregar').classList.add('show');
}

window.cerrarModalAgregar = function() {
    document.getElementById('modalAgregar').classList.remove('show');
}

window.confirmarEliminar = function(productoId, nombre) {
    if (confirm(`¿Estás seguro de eliminar el producto "${nombre}"?`)) {
        // Construir la URL correctamente
        const urlBase = "{% url 'admin_eliminar_producto' 0 %}";
        const urlFinal = urlBase.replace('/0/', `/${productoId}/`);
        
        // Enviar formulario o hacer petición
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = urlFinal;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            form.appendChild(csrfToken.cloneNode());
        }
        
        document.body.appendChild(form);
        form.submit();
    }
}

window.cerrarModalEliminar = function() {
    document.getElementById('modalEliminar').classList.remove('show');
}

window.previewImage = function(input) {
    const preview = document.getElementById('imagePreview');
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.add('show');
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        preview.src = '';
        preview.classList.remove('show');
    }
}