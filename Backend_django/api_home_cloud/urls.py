from django.urls import path
from rest_framework import routers
from .api import (
    UsuarioViewSet,
    GrupoViewSet,
    PerfilUsuarioViewSet,
    DocumentoViewSet,
    TareaViewSet,
    NotificacionViewSet,
)
from .views import (
    azure_storage_status,
    list_files,
    upload_file,
    download_file,
    delete_file,
    get_file_url,
    test_azure_storage,
)

# Creamos el router de DRF
router = routers.DefaultRouter()

# Registramos todos los endpoints
router.register('api/usuarios', UsuarioViewSet, basename='usuarios')
router.register('api/grupos', GrupoViewSet, basename='grupos')
router.register('api/perfiles', PerfilUsuarioViewSet, basename='perfiles')
router.register('api/documentos', DocumentoViewSet, basename='documentos')
router.register('api/tareas', TareaViewSet, basename='tareas')
router.register('api/notificaciones', NotificacionViewSet, basename='notificaciones')

# Incluimos todas las rutas generadas automáticamente
urlpatterns = router.urls

# URLs para Azure Storage
urlpatterns += [
    path('api/azure/status/', azure_storage_status, name='azure_status'),
    path('api/azure/test/', test_azure_storage, name='azure_test'),
    path('api/azure/files/', list_files, name='azure_list_files'),
    path('api/azure/files/upload/', upload_file, name='azure_upload_file'),
    path('api/azure/files/<str:blob_name>/download/', download_file, name='azure_download_file'),
    path('api/azure/files/<str:blob_name>/delete/', delete_file, name='azure_delete_file'),
    path('api/azure/files/<str:blob_name>/url/', get_file_url, name='azure_get_file_url'),
]