from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Grupo, PerfilUsuario, Documento, Tarea, Notificacion
from .serializers import (
    UsuarioSerializer,
    GrupoSerializer,
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

# Grupos
class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all().order_by('-fecha_creacion')
    serializer_class = GrupoSerializer
    permission_classes = [permissions.AllowAny]

# Perfiles de usuario
class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.select_related('user', 'grupo').all()
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [permissions.AllowAny]

# Documentos
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.select_related('grupo', 'usuario').all().order_by('-fecha_subida')
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
    queryset = Tarea.objects.select_related('grupo', 'documento', 'creado_por', 'asignado_a').all().order_by('-fecha_creacion')
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