from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail # Enviar un correo con los datos
from django.db.models import Q 
import uuid
from .models import (
    Producto, Combustible, TipoMezcla, TipoCompactacion, TipoCorte,
    TipoDemoledor, TipoAlisador, TipoVibrador, TipoElevacion,
    TipoCarga, TipoGenerador, TipoEquiposEspeciales
)

PROCESO_MAPPING = {
    'MEZCLA': {'modelo': 'mezcla', 'tipo_modelo': TipoMezcla},
    'COMPACTACION': {'modelo': 'compactacion', 'tipo_modelo': TipoCompactacion},
    'CORTE': {'modelo': 'cortadora', 'tipo_modelo': TipoCorte},
    'DEMOLEDORA': {'modelo': 'demoledor', 'tipo_modelo': TipoDemoledor},
    'ALISADOR': {'modelo': 'alisador', 'tipo_modelo': TipoAlisador},
    'VIBRADORES': {'modelo': 'vibrador', 'tipo_modelo': TipoVibrador},
    'ELEVACION': {'modelo': 'elevacion', 'tipo_modelo': TipoElevacion},
    'CARGA': {'modelo': 'carga', 'tipo_modelo': TipoCarga},
    'GENERADOR': {'modelo': 'generador', 'tipo_modelo': TipoGenerador},
    'EQUIPOS_ESPECIALES': {'modelo': 'equiposespeciales', 'tipo_modelo': TipoEquiposEspeciales},
}

def inicio(request):
    """
    Vista principal para mostrar los productos destacados en la página de inicio.
    """
    # Obtener los productos con más "Me Gusta"
    productos = Producto.objects.all().order_by('-cantidad_me_gusta')[:3]

    # Añadir información adicional a cada producto
    for producto in productos:
        for proceso_info in PROCESO_MAPPING.values():
            modelo = proceso_info['modelo']
            if hasattr(producto, modelo) and getattr(producto, modelo):
                producto.combustible = getattr(producto, modelo).combustible
                break

    # Contexto para la plantilla
    context = {
        'productos': productos,
        'combustibles': Combustible.choices,
    }

    return render(request, 'inicio/inicio.html', context)
    

def nosotros(request):
    return render(request, 'inicio/nosotros.html')

def contacto(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Procesar los datos (enviar correo, guardar en base de datos, etc.)
        # Ejemplo de enviar un correo:
        send_mail(
            'Nuevo mensaje de contacto',
            f'Nombre: {name}\nCorreo: {email}\nMensaje: {message}',
            'framqueli@gmail.com',  # Cambiar por tu correo
            ['framqueli@gmail.com'],  # Cambiar por el correo destinatario
            fail_silently=False,
        )

        return HttpResponse("Gracias por tu mensaje, nos pondremos en contacto pronto.")
    return render(request, 'inicio/contacto.html')


def producto_detail(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtener el combustible según el proceso
    combustible = None
    proceso_modelo = {
        'Alisador': 'alisador',
        'Carga': 'carga',
        'Compactación': 'compactacion',
        'Corte': 'cortadora',
        'Demoledora': 'demoledor',
        'Elevación': 'elevacion',
        'Equipos Especiales': 'equipos especiales',
        'Generador': 'generador',
        'Mezcla': 'mezcla',
        'Vibradores': 'vibrador',
    }
    
    if producto.procesos in proceso_modelo:
        modelo_relacionado = getattr(producto, proceso_modelo[producto.procesos], None)
        if modelo_relacionado:
            combustible = modelo_relacionado.combustible

    # Manejo de cookies para los likes (código existente)
    user_cookie = request.COOKIES.get('user_cookie', None)
    if not user_cookie:
        user_cookie = str(uuid.uuid4())
        response = render(request, 'inicio/producto_detail.html', {
            'producto': producto,
            'combustible': combustible
        })
        response.set_cookie('user_cookie', user_cookie, max_age=60*60*24*365)
    else:
        response = render(request, 'inicio/producto_detail.html', {
            'producto': producto,
            'combustible': combustible
        })

    liked_products = request.COOKIES.get(f'liked_products_{user_cookie}', '').split(',')
    producto_liked = str(producto.id) in liked_products

    if request.method == 'POST' and not producto_liked:
        producto.cantidad_me_gusta += 1
        producto.save()
        liked_products.append(str(producto.id))
        response.set_cookie(f'liked_products_{user_cookie}', ','.join(liked_products), max_age=60*60*24*365)
        return JsonResponse({'success': True, 'likes_count': producto.cantidad_me_gusta})

    context = {
        'producto': producto,
        'producto_liked': producto_liked,
        'combustible': combustible
    }
    return render(request, 'inicio/producto_detail.html', context)





# Mapeo de procesos a modelos y campos
PROCESO_MAPPING = {
    'ALISADOR': {
        'modelo': 'alisador',
        'tipo_modelo': TipoAlisador,
        'campos_adicionales': ['capacidad']
    },
    'CARGA': {
        'modelo': 'carga',
        'tipo_modelo': TipoCarga,
        'campos_adicionales': ['capacidad', 'implementos']
    },
    'COMPACTACION': {
        'modelo': 'compactacion',
        'tipo_modelo': TipoCompactacion,
        'campos_adicionales': ['tamaño', 'potencia_compactacion']
    },
    'CORTE': {
        'modelo': 'cortadora',
        'tipo_modelo': TipoCorte,
        'campos_adicionales': ['profundidad']
    },
    'DEMOLEDORA': {
        'modelo': 'demoledor',
        'tipo_modelo': TipoDemoledor,
        'campos_adicionales': ['capacidad', 'tamaño']
    },
    'ELEVACION': {
        'modelo': 'elevacion',
        'tipo_modelo': TipoElevacion,
        'campos_adicionales': ['altura', 'uso']
    },
    'EQUIPOS_ESPECIALES': {
        'modelo': 'equiposespeciales',
        'tipo_modelo': TipoEquiposEspeciales,
    },
    'MEZCLA': {
        'modelo': 'mezcla',
        'tipo_modelo': TipoMezcla,
        'campos_adicionales': ['capacidad']
    },
    'GENERADOR': {
        'modelo': 'generador',
        'tipo_modelo': TipoGenerador,
        'campos_adicionales': ['capacidad', 'uso', 'kilowatts']
    },
    'VIBRADORES': {
        'modelo': 'vibrador',
        'tipo_modelo': TipoVibrador,
        'campos_adicionales': ['capacidad']
    },
}

def get_proceso_info(proceso):
    """Obtiene la información de mapeo para un proceso específico"""
    return PROCESO_MAPPING.get(proceso, {})

def obtener_tipos(request):
    """Vista para obtener tipos de proceso vía AJAX"""
    proceso = request.GET.get('proceso')
    proceso_info = get_proceso_info(proceso)
    
    if not proceso_info:
        return JsonResponse({'tipos': []})
    
    tipos = proceso_info['tipo_modelo'].objects.filter(activo=True)
    tipos_data = [{'id': tipo.id, 'nombre': tipo.nombre} for tipo in tipos]
    
    # Obtener campos adicionales si existen
    campos_adicionales = {}
    if proceso_info.get('campos_adicionales'):
        modelo_relacionado = proceso_info['modelo']
        for campo in proceso_info['campos_adicionales']:
            valores = Producto.objects.filter(procesos=proceso)\
                .values_list(f'{modelo_relacionado}__{campo}', flat=True)\
                .distinct()
            campos_adicionales[campo] = list(valores)
    
    return JsonResponse({
        'tipos': tipos_data,
        'campos_adicionales': campos_adicionales
    })

def productos(request):
    """Vista principal de productos con filtros dinámicos y búsqueda"""
    productos = Producto.objects.all()
    context = {}
    
    # Obtener término de búsqueda
    search_query = request.GET.get('search', '').strip()
    
    # Aplicar búsqueda si existe un término
    if search_query:
        productos = productos.filter(
            Q(nombre__icontains=search_query) |
            Q(descripcion__icontains=search_query)
        ).distinct()
    
    # Obtener filtros básicos
    proceso = request.GET.get('procesos')
    tipo_id = request.GET.get('tipo')
    categoria = request.GET.get('categoria')
    estado = request.GET.get('estado')
    combustible = request.GET.get('combustible')
    
    # Aplicar filtros básicos
    if proceso:
        productos = productos.filter(procesos=proceso)
        proceso_info = get_proceso_info(proceso)
        
        if proceso_info:
            if tipo_id:
                productos = productos.filter(**{
                    f"{proceso_info['modelo']}__tipo_id": tipo_id
                })
            
            for campo in proceso_info.get('campos_adicionales', []):
                valor_campo = request.GET.get(campo)
                if valor_campo:
                    productos = productos.filter(**{
                        f"{proceso_info['modelo']}__{campo}": valor_campo
                    })
                
                valores = productos.values_list(
                    f"{proceso_info['modelo']}__{campo}",
                    flat=True
                ).distinct()
                context[f'{campo}_valores'] = valores
    
    # Aplicar resto de filtros
    if categoria:
        productos = productos.filter(categoria=categoria)
    if estado:
        productos = productos.filter(estado=estado)
    
    if combustible:
        q_combustible = Q()
        for proceso_info in PROCESO_MAPPING.values():
            q_combustible |= Q(**{f"{proceso_info['modelo']}__combustible": combustible})
        productos = productos.filter(q_combustible)
    
    # Añadir combustible a cada producto
    for producto in productos:
        for proceso_info in PROCESO_MAPPING.values():
            modelo = proceso_info['modelo']
            if hasattr(producto, modelo) and getattr(producto, modelo):
                producto.combustible = getattr(producto, modelo).combustible
                break
    
    # Actualizar contexto
    context.update({
        'productos': productos,
        'combustibles': Combustible.choices,
        'categorias': Producto.CATEGORIA_CHOICES,
        'estados': Producto.ESTADO_CHOICES,
        'procesos': dict(Producto.PROCESOS_CHOICES),
        'proceso_actual': proceso,
        'tipo_actual': tipo_id,
        'categoria_actual': categoria,
        'estado_actual': estado,
        'combustible_actual': combustible,
        'search_query': search_query,
    })
    
    return render(request, 'inicio/productos.html', context)

def ver_carrito(request):
    return render(request, 'carrito/ver_carrito.html')