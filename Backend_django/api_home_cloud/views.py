from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
from .azure_storage import azure_storage

# Create your views here.

@require_http_methods(["GET"])
def azure_storage_status(request):
    """
    Verifica el estado de la conexión con Azure Storage
    """
    is_configured = azure_storage.blob_service_client is not None

    return JsonResponse({
        'azure_storage_configured': is_configured,
        'container_name': azure_storage.container_name if is_configured else None,
        'account_name': azure_storage.account_name if is_configured else None,
    })

@require_http_methods(["GET"])
def list_files(request):
    """
    Lista archivos en Azure Storage
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado'
        }, status=500)

    prefix = request.GET.get('prefix', '')
    files = azure_storage.list_files(prefix)

    return JsonResponse({
        'files': files,
        'total': len(files)
    })

@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    """
    Sube un archivo a Azure Storage
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado'
        }, status=500)

    if 'file' not in request.FILES:
        return JsonResponse({
            'error': 'No se encontró el archivo en la solicitud'
        }, status=400)

    file_obj = request.FILES['file']
    blob_name = request.POST.get('blob_name', file_obj.name)

    # Determinar el tipo de contenido
    content_type = file_obj.content_type or 'application/octet-stream'

    # Subir el archivo
    url = azure_storage.upload_file(file_obj, blob_name, content_type)

    if url:
        return JsonResponse({
            'message': 'Archivo subido exitosamente',
            'blob_name': blob_name,
            'url': url,
            'content_type': content_type
        })
    else:
        return JsonResponse({
            'error': 'Error al subir el archivo'
        }, status=500)

@require_http_methods(["GET"])
def download_file(request, blob_name):
    """
    Descarga un archivo desde Azure Storage
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado'
        }, status=500)

    data = azure_storage.download_file(blob_name)

    if data is None:
        return JsonResponse({
            'error': 'Archivo no encontrado'
        }, status=404)

    # Crear respuesta con el archivo
    response = HttpResponse(data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{blob_name}"'

    return response

@require_http_methods(["DELETE"])
def delete_file(request, blob_name):
    """
    Elimina un archivo de Azure Storage
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado'
        }, status=500)

    success = azure_storage.delete_file(blob_name)

    if success:
        return JsonResponse({
            'message': f'Archivo {blob_name} eliminado exitosamente'
        })
    else:
        return JsonResponse({
            'error': f'Error al eliminar el archivo {blob_name}'
        }, status=500)

@require_http_methods(["GET"])
def get_file_url(request, blob_name):
    """
    Obtiene la URL de un archivo en Azure Storage
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado'
        }, status=500)

    url = azure_storage.get_file_url(blob_name)

    if url:
        return JsonResponse({
            'blob_name': blob_name,
            'url': url
        })
    else:
        return JsonResponse({
            'error': 'Archivo no encontrado'
        }, status=404)

# Vista de prueba simple para verificar que todo funciona
@require_http_methods(["GET"])
def test_azure_storage(request):
    """
    Prueba básica de Azure Storage - crea un archivo de prueba
    """
    if not azure_storage.blob_service_client:
        return JsonResponse({
            'error': 'Azure Storage no está configurado. Verifica tus variables de entorno.'
        }, status=500)

    # Crear un archivo de prueba
    test_content = b"Hola desde Azure Storage! Esta es una prueba de conectividad."
    test_blob_name = "test_file.txt"

    # Usar io.BytesIO para simular un file-like object
    from io import BytesIO
    test_file = BytesIO(test_content)

    url = azure_storage.upload_file(test_file, test_blob_name, "text/plain")

    if url:
        # Verificar que podemos descargar el archivo
        downloaded_content = azure_storage.download_file(test_blob_name)

        success = downloaded_content == test_content

        return JsonResponse({
            'message': 'Prueba de Azure Storage exitosa!',
            'test_file_url': url,
            'upload_success': True,
            'download_success': success,
            'content_matches': success,
            'container_name': azure_storage.container_name
        })
    else:
        return JsonResponse({
            'error': 'Error en la prueba de subida',
            'upload_success': False
        }, status=500)
