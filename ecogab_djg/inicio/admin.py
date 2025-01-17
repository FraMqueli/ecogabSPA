from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse_lazy
from .models import (
    Producto, Compactacion, Mezcla, Cortadora, Demoledor, Alisador, Vibrador, 
    Elevacion, Carga, EquiposEspeciales, Generador,
    TipoCompactacion, TipoMezcla, TipoCorte, TipoDemoledor, TipoAlisador, 
    TipoVibrador, TipoElevacion, TipoCarga, TipoEquiposEspeciales, TipoGenerador
)

# Admin para tipos base
class TipoBaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información Principal', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Información Temporal', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

# Registrar todos los tipos usando el TipoBaseAdmin
admin.site.register(TipoCompactacion, TipoBaseAdmin)
admin.site.register(TipoMezcla, TipoBaseAdmin)
admin.site.register(TipoCorte, TipoBaseAdmin)
admin.site.register(TipoDemoledor, TipoBaseAdmin)
admin.site.register(TipoAlisador, TipoBaseAdmin)
admin.site.register(TipoVibrador, TipoBaseAdmin)
admin.site.register(TipoElevacion, TipoBaseAdmin)
admin.site.register(TipoCarga, TipoBaseAdmin)
admin.site.register(TipoEquiposEspeciales, TipoBaseAdmin)
admin.site.register(TipoGenerador, TipoBaseAdmin)

# Inlines para equipos
class EquipoBaseInline(admin.StackedInline):
    extra = 0
    can_delete = False
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
class DemoledorInline(EquipoBaseInline):
    model = Demoledor
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad', 'tamaño')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class AlisadorInline(EquipoBaseInline):
    model = Alisador
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad',)
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class VibradorInline(EquipoBaseInline):
    model = Vibrador
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad',)
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class ElevacionInline(EquipoBaseInline):
    model = Elevacion
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('altura', 'uso')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class CargaInline(EquipoBaseInline):
    model = Carga
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad', 'implementos')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class GeneradorInline(EquipoBaseInline):
    model = Generador
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad', 'uso', 'kilowatts')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class EquiposEspecialesInline(EquipoBaseInline):
    model = EquiposEspeciales
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('caracteristicas_especiales',)
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
class CompactacionInline(EquipoBaseInline):
    model = Compactacion
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('tamaño', 'potencia_compactacion', 'kilowatts')
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class MezclaInline(EquipoBaseInline):
    model = Mezcla
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('capacidad',)
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class CortadoraInline(EquipoBaseInline):
    model = Cortadora
    fieldsets = (
        ('Información Principal', {
            'fields': ('tipo', 'combustible', 'modelo')
        }),
        ('Especificaciones', {
            'fields': ('profundidad',)
        }),
        ('Notas y Fechas', {
            'fields': ('notas', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

class DemoledorInline(EquipoBaseInline):
    model = Demoledor

class AlisadorInline(EquipoBaseInline):
    model = Alisador

class VibradorInline(EquipoBaseInline):
    model = Vibrador

class ElevacionInline(EquipoBaseInline):
    model = Elevacion

class CargaInline(EquipoBaseInline):
    model = Carga

class GeneradorInline(EquipoBaseInline):
    model = Generador

class EquiposEspecialesInline(EquipoBaseInline):
    model = EquiposEspeciales

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('enlace_detalles',)

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'estado', 'categoria', 'procesos')
        }),
        ('Precios y Estadísticas', {
            'fields': ('precio', 'cantidad_me_gusta')
        }),
        ('Multimedia', {
            'fields': ('imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'video_url')
        }),
    )

    list_display = ('nombre', 'precio', 'estado', 'categoria', 'procesos', 'cantidad_me_gusta')
    list_filter = ('categoria', 'estado', 'procesos')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-cantidad_me_gusta',)

    def get_inline_instances(self, request, obj=None):
        if not obj or not obj.procesos:
            return []

        inlines_map = {
            'COMPACTACION': CompactacionInline,
            'MEZCLA': MezclaInline,
            'CORTE': CortadoraInline,
            'DEMOLEDORA': DemoledorInline,
            'ALISADOR': AlisadorInline,
            'VIBRADORES': VibradorInline,
            'ELEVACION': ElevacionInline,
            'CARGA': CargaInline,
            'EQUIPOS_ESPECIALES': EquiposEspecialesInline,
            'GENERADOR': GeneradorInline,
        }

        inline_class = inlines_map.get(obj.procesos)
        if inline_class:
            return [inline_class(self.model, self.admin_site)]
        return []

    class Media:
        js = ('admin/js/jquery.init.js',)
        css = {
            'all': ('admin/css/forms.css',)
        }
        extra = [
            '''
            <script>
            django.jQuery(document).ready(function($) {
                function updateInlines() {
                    var selectedProceso = $('#id_procesos').val();
                    $('.inline-group').hide();
                    
                    if (selectedProceso) {
                        $('.inline-group').each(function() {
                            var className = $(this).attr('class').toLowerCase();
                            if (className.indexOf(selectedProceso.toLowerCase()) !== -1) {
                                $(this).show();
                            }
                        });
                    }
                }
                
                $('#id_procesos').change(updateInlines);
                updateInlines();
            });
            </script>
            '''
        ]

# admin.py




class CustomAdminSite(AdminSite):
    login_template = 'custom_admin/loing.html'
    
    def login(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['password_reset_url'] = reverse_lazy('password_reset')
        return super().login(request, extra_context)

# Crear la instancia del admin personalizado
admin_site = CustomAdminSite()

# Copiar todos los modelos registrados del admin original al nuevo
for model, model_admin in admin.site._registry.items():
    admin_site.register(model, type(model_admin))

# Reemplazar el sitio admin predeterminado
admin.site = admin_site