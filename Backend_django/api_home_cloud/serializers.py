from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Familia, PerfilUsuario, Documento, Tarea, Notificacion

#convierte objetos Django a estructuras simples (diccionarios/JSON) para API y viceversa (decodificar JSON en datos Python para crear/actualizar modelos).

# Serializer del usuario base (de Django)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# Familia
class FamiliaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Familia
        fields = ['id', 'nombre', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


# PerfilUsuario
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    user = UsuarioSerializer(read_only=True)
    familia = serializers.PrimaryKeyRelatedField(queryset=Familia.objects.all())

    class Meta:
        model = PerfilUsuario
        fields = ['id', 'user', 'familia', 'rol']
        read_only_fields = ['id']


# Documento
class DocumentoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    familia = serializers.PrimaryKeyRelatedField(queryset=Familia.objects.all())

    class Meta:
        model = Documento
        fields = [
            'id', 'familia', 'usuario', 'nombre_archivo', 'url_archivo',
            'tipo_documento', 'fecha_subida', 'procesado'
        ]
        read_only_fields = ['id', 'fecha_subida', 'procesado']


# Tarea
class TareaSerializer(serializers.ModelSerializer):
    creado_por = UsuarioSerializer(read_only=True)
    asignado_a = UsuarioSerializer(read_only=True)
    documento = serializers.PrimaryKeyRelatedField(
        queryset=Documento.objects.all(), allow_null=True, required=False
    )
    familia = serializers.PrimaryKeyRelatedField(queryset=Familia.objects.all())

    class Meta:
        model = Tarea
        fields = [
            'id', 'familia', 'documento', 'titulo', 'descripcion',
            'fecha_vencimiento', 'monto', 'estado', 'creado_por',
            'asignado_a', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion']


# Notificación
class NotificacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    tarea = serializers.PrimaryKeyRelatedField(queryset=Tarea.objects.all())

    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'tarea', 'mensaje', 'fecha_envio', 'leida']
        read_only_fields = ['id', 'fecha_envio']
