from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import IntegrityError
from .models import *
class CorporacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporacion
        fields = '__all__'

class Donador_CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donador_Categoria
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Evento
        fields = '__all__'

    def validate(self, attrs):
        fecha_inicio = attrs.get('fecha_inicio')
        fecha_fin = attrs.get('fecha_fin')
        if self.instance:
            fecha_inicio = fecha_inicio or self.instance.fecha_inicio
            fecha_fin = fecha_fin or self.instance.fecha_fin
        
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise serializers.ValidationError(detail={'fecha_fin':'lesser_than_fecha_inicio'}, code=400)
        
        return super().validate(attrs)

class DonadorSerializer(serializers.ModelSerializer):
    categoria_display = serializers.StringRelatedField(source='categoria')
    id_corporacion_display = serializers.StringRelatedField(source='id_corporacion')
    id_clase_display = serializers.StringRelatedField(source='id_clase')
    id_corporacion_conyuge_display = serializers.StringRelatedField(source='id_corporacion_conyuge')
    class Meta:
        model = Donador
        fields = '__all__'

class EventoDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clase
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            for validator in field.validators:
                if isinstance(validator, UniqueValidator):
                    validator.message = f'Ya existe un registro con ese {field_name}.'

#OPTIONS DE SELECTS
class Donador_CategoriaDisplaySerializer(serializers.ModelSerializer):
    display = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    class Meta:
        model = Donador_Categoria
        fields = ['key', 'display']
    
    def get_key(self, obj):
        return obj.id
    def get_display(self, obj):
        return f"{obj.id}: {obj.nombre}"

class CorporacionDisplaySerializer(serializers.ModelSerializer):
    display = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    class Meta:
        model = Corporacion
        fields = ['key', 'display']
    
    def get_key(self, obj):
        return obj.id
    def get_display(self, obj):
        return f"{obj.id}: {obj.nombre}"
    
class EventoDisplaySerializer(serializers.ModelSerializer):
    display = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    class Meta:
        model = Evento
        fields = ['key', 'display']
    
    def get_key(self, obj):
        return obj.id
    
    def get_display(self, obj):
        return f"{obj.id}: {obj.nombre} - {obj.tipo} ({obj.fecha_inicio} - {obj.fecha_fin})"

class ClaseDisplaySerializer(serializers.ModelSerializer):
    display = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    class Meta:
        model = Corporacion
        fields = ['key', 'display']
    
    def get_key(self, obj):
        return obj.anio_graduacion
    def get_display(self, obj):
        return f"{obj.anio_graduacion}"
    
    

class UserioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userio
        fields = '__all__'
    
    def create(self, validated_data):
        try:
            usr = Userio.objects.create_user(**validated_data)
            validated_data['rol'] = 'admin'
            if 'rol' in validated_data and validated_data['rol'] == 'admin': usr.is_staff = True
            return usr
        
        except IntegrityError as e:
            self._handle_integrity_error(e)

    def _handle_integrity_error(self, e: IntegrityError):
        error = str(e).lower()
        if 'unique' in error:
            raise serializers.ValidationError({
                error:{'detail':'Este usuario ya existe'}
            })
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        usr:Userio = super().update(instance, validated_data)

        #cifrao
        if password:
            usr.set_password(password)

        if 'rol' in validated_data and validated_data['rol'] == 'admin': usr.is_staff = True
        else: usr.is_staff = False
        usr.save()
        return usr

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Userio
        fields = ['username', 'password']
    
    def create(self, validated_data):
        validated_data['rol'] = 'admin'
        usr = Userio.objects.create_user(**validated_data)
        if 'rol' in validated_data and validated_data['rol'] == 'admin': usr.is_staff = True
        return usr