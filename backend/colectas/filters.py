import django_filters

from colectas.models import *

class CorporacionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    direccion = django_filters.CharFilter(lookup_expr='icontains')
    telefono = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Corporacion
        fields = [
            'id',
            'nombre',
            'direccion',
            'telefono',
            'email',
        ]

class Donador_CategoriaFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Donador_Categoria
        fields = ['id']

class EventoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    fecha_inicio = django_filters.DateFilter(lookup_expr='icontains')
    fecha_fin = django_filters.DateFilter(lookup_expr='icontains')
    tipo = django_filters.CharFilter(lookup_expr='icontains')
    descripcion = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Evento
        fields = ['id']

class DonadorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    primer_ap = django_filters.CharFilter(lookup_expr='icontains')
    segundo_ap = django_filters.CharFilter(lookup_expr='icontains')
    direccion = django_filters.CharFilter(lookup_expr='icontains')
    telefono = django_filters.NumberFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.NumberFilter(lookup_expr='icontains')
    anio_graduacion = django_filters.NumberFilter(lookup_expr='icontains')
    id_clase = django_filters.NumberFilter(lookup_expr='icontains')
    id_corporacion = django_filters.NumberFilter(lookup_expr='icontains')
    nombre_conyuge = django_filters.CharFilter(lookup_expr='icontains')
    id_corporacion_conyuge = django_filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Donador
        fields = ['nombre']

class ClaseFilter(django_filters.FilterSet):
    anio_graduacion = django_filters.NumberFilter(lookup_expr='icontains')

    class Meta:
        model = Clase
        fields = ['anio_graduacion']

class UserioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    rol = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Userio
        fields = ['username']