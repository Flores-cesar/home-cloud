from rest_framework import routers
from .api import (
    UsuarioViewSet,
    FamiliaViewSet,
    PerfilUsuarioViewSet,
    DocumentoViewSet,
    TareaViewSet,
    NotificacionViewSet,
)

# Creamos el router de DRF
router = routers.DefaultRouter()

# Registramos todos los endpoints
router.register('api/usuarios', UsuarioViewSet, basename='usuarios')
router.register('api/familias', FamiliaViewSet, basename='familias')
router.register('api/perfiles', PerfilUsuarioViewSet, basename='perfiles')
router.register('api/documentos', DocumentoViewSet, basename='documentos')
router.register('api/tareas', TareaViewSet, basename='tareas')
router.register('api/notificaciones', NotificacionViewSet, basename='notificaciones')

# Incluimos todas las rutas generadas automáticamente
urlpatterns = router.urls
