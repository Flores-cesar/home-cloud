from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Familia, PerfilUsuario, Documento, Tarea, Notificacion
from .serializers import (
    UsuarioSerializer,
    FamiliaSerializer,
    PerfilUsuarioSerializer,
    DocumentoSerializer,
    TareaSerializer,
    NotificacionSerializer,
)

# ModelViewSet agrupa la lógica CRUD porque hereda/componen su comportamiento desde varias clases (mixins) que implementan cada operación.
# Usa routers (DefaultRouter) para enrutar automáticamente los actions del viewset.

# Usuarios (solo lectura)
class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.AllowAny]

# Familias
class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all().order_by('-fecha_creacion')
    serializer_class = FamiliaSerializer
    permission_classes = [permissions.AllowAny]

# Perfiles de usuario
class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.select_related('user', 'familia').all()
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [permissions.AllowAny]

# Documentos
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.select_related('familia', 'usuario').all().order_by('-fecha_subida')
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.AllowAny]

    # si querés que el usuario logueado sea automáticamente el "uploader"
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()

# Tareas
class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.select_related('familia', 'documento', 'creado_por', 'asignado_a').all().order_by('-fecha_creacion')
    serializer_class = TareaSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(creado_por=self.request.user)
        else:
            serializer.save()

# Notificaciones
class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.select_related('usuario', 'tarea').all().order_by('-fecha_envio')
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.AllowAny]