from django.db import models
from django.urls import reverse
import re

# Modelo para tipos de combustibles
class Combustible(models.TextChoices):
    DIESEL = 'Diesel', 'Diesel'
    BENCINA = 'Bencina', 'Bencina'
    ELECTRICO = 'Eléctrico', 'Eléctrico'

# Modelo base para tipos
class TipoBase(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre

# Tipos específicos para cada categoría
class TipoCompactacion(TipoBase):
    class Meta:
        verbose_name = "Tipo de Compactación"
        verbose_name_plural = "Tipos de Compactación"

class TipoMezcla(TipoBase):
    class Meta:
        verbose_name = "Tipo de Mezcla"
        verbose_name_plural = "Tipos de Mezcla"

class TipoCorte(TipoBase):
    class Meta:
        verbose_name = "Tipo de Corte"
        verbose_name_plural = "Tipos de Corte"

class TipoDemoledor(TipoBase):
    class Meta:
        verbose_name = "Tipo de Demoledor"
        verbose_name_plural = "Tipos de Demoledor"

class TipoAlisador(TipoBase):
    class Meta:
        verbose_name = "Tipo de Alisador"
        verbose_name_plural = "Tipos de Alisador"

class TipoVibrador(TipoBase):
    class Meta:
        verbose_name = "Tipo de Vibrador"
        verbose_name_plural = "Tipos de Vibrador"

class TipoElevacion(TipoBase):
    class Meta:
        verbose_name = "Tipo de Elevación"
        verbose_name_plural = "Tipos de Elevación"

class TipoCarga(TipoBase):
    class Meta:
        verbose_name = "Tipo de Carga"
        verbose_name_plural = "Tipos de Carga"

class TipoGenerador(TipoBase):
    class Meta:
        verbose_name = "Tipo de Generador"
        verbose_name_plural = "Tipos de Generador"

class TipoEquiposEspeciales(TipoBase):
    class Meta:
        verbose_name = "Tipo de Equipo Especial"
        verbose_name_plural = "Tipos de Equipos Especiales"

# Modelo base para equipos
class EquipoBase(models.Model):
    producto = models.OneToOneField('Producto', on_delete=models.CASCADE)
    combustible = models.CharField(max_length=20, choices=Combustible.choices)
    modelo = models.CharField(max_length=50)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Modelos específicos para cada equipo
class Compactacion(EquipoBase):
    tipo = models.ForeignKey(TipoCompactacion, on_delete=models.PROTECT)
    tamaño = models.CharField(max_length=50)
    potencia_compactacion = models.CharField(max_length=50)
    kilowatts = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class Mezcla(EquipoBase):
    tipo = models.ForeignKey(TipoMezcla, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)

class Cortadora(EquipoBase):
    tipo = models.ForeignKey(TipoCorte, on_delete=models.PROTECT)
    profundidad = models.DecimalField(max_digits=5, decimal_places=2)

class Demoledor(EquipoBase):
    tipo = models.ForeignKey(TipoDemoledor, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=50)

class Alisador(EquipoBase):
    tipo = models.ForeignKey(TipoAlisador, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)

class Vibrador(EquipoBase):
    tipo = models.ForeignKey(TipoVibrador, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)

class Elevacion(EquipoBase):
    tipo = models.ForeignKey(TipoElevacion, on_delete=models.PROTECT)
    altura = models.CharField(max_length=50)
    uso = models.CharField(max_length=50)

class Carga(EquipoBase):
    tipo = models.ForeignKey(TipoCarga, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)
    implementos = models.CharField(max_length=100)

class Generador(EquipoBase):
    tipo = models.ForeignKey(TipoGenerador, on_delete=models.PROTECT)
    capacidad = models.CharField(max_length=50)
    uso = models.CharField(max_length=50)
    kilowatts = models.DecimalField(max_digits=5, decimal_places=2)

class EquiposEspeciales(EquipoBase):
    tipo = models.ForeignKey(TipoEquiposEspeciales, on_delete=models.PROTECT)
    caracteristicas_especiales = models.TextField()

# El modelo Producto permanece igual pero actualizado para reflejar las relaciones
class Producto(models.Model):
    DISPONIBLE = 'Disponible'
    NO_DISPONIBLE = 'No disponible'
    EN_ARRIENDO = 'En arriendo'
    PARA_IMPORTAR = 'Para Importar'
    ESTADO_CHOICES = [
        (DISPONIBLE, 'Disponible'),
        (NO_DISPONIBLE, 'No disponible'),
        (EN_ARRIENDO, 'En arriendo'),
        (PARA_IMPORTAR, 'Para Importar'),
    ]

    VENTA = 'Venta'
    ARRIENDO = 'Arriendo'
    CATEGORIA_CHOICES = [
        (VENTA, 'Venta'),
        (ARRIENDO, 'Arriendo'),
    ]
    COMBUSTIBLE_CHOICES = [
        ('Gasolina', 'Gasolina'),
        ('Diesel', 'Diesel'),
        ('Eléctrico', 'Eléctrico'),
    ]
    combustible = models.CharField(
        max_length=20,
        choices=COMBUSTIBLE_CHOICES,
        default='Gasolina'
    )
    PROCESOS_CHOICES = [
        ('ALISADOR', 'Alisador'),
        ('CARGA', 'Carga'),
        ('COMPACTACION', 'Compactación'),
        ('CORTE', 'Corte'),
        ('DEMOLEDORA', 'Demoledora'),
        ('ELEVACION', 'Elevación'),
        ('EQUIPOS_ESPECIALES', 'Equipos Especiales'),
        ('GENERADOR', 'Generador'),
        ('MEZCLA', 'Mezcla'),
        ('VIBRADORES', 'Vibradores'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen_1 = models.ImageField(upload_to='productos/')
    imagen_2 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen_3 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen_4 = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen_5 = models.ImageField(upload_to='productos/', null=True, blank=True)
    video_url = models.CharField(max_length=200)
    cantidad_me_gusta = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    enlace_detalles = models.URLField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=DISPONIBLE)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default=VENTA)
    procesos = models.CharField(max_length=20, choices=PROCESOS_CHOICES)

    def save(self, *args, **kwargs):
        youtube_regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(youtube_regex, self.video_url)
        if match:
            self.video_url = match.group(1)

        if self.categoria == self.ARRIENDO:
            self.precio = None
        
        super().save(*args, **kwargs)

    def get_video_thumbnail(self):
        return f'https://img.youtube.com/vi/{self.video_url}/0.jpg'
    
    def __str__(self):
        return self.nombre