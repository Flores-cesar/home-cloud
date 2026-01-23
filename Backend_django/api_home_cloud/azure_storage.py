import os
import logging
from typing import List, Optional, BinaryIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from django.conf import settings

# Instancias BlobServiceClient (Te conectas a Azure). ↓
# Le pides al servicio un ContainerClient (Eliges la carpeta "media"). ↓
# Le pides al contenedor un BlobClient (Reservas el nombre "foto.jpg"). ↓
##Se crea especificando: contenedor + nombre del archivo
# Usas el blob client para hacer el upload.

logger = logging.getLogger(__name__)

class AzureStorageService:
    """
    Clase de servicio que encapsula la interacción con la API de Azure Blob Storage.
    """
    def __init__(self):
        """
        Constructor de la clase.
        Realiza la inyección de dependencias de configuración obteniendo las credenciales
        desde `django.conf.settings`. Inicializa el `BlobServiceClient` mediante
        Connection String o par Account Name/Key.
        """
        # Recuperación segura de constantes de configuración mediante getattr (evita AttributeError)
        self.account_name = getattr(settings, 'AZURE_STORAGE_ACCOUNT_NAME', None)
        self.account_key = getattr(settings, 'AZURE_STORAGE_ACCOUNT_KEY', None)
        self.connection_string = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
        self.container_name = getattr(settings, 'AZURE_STORAGE_CONTAINER_NAME', 'files')
        # Validación de integridad de la configuración antes de intentar la conexión
        if not self._is_configured():
            logger.warning("Azure Storage no está configurado correctamente")
            self.blob_service_client = None
            return

        try:
            # Prioridad a Connection String sobre Account Key
            if self.connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            else:
                account_url = f"https://{self.account_name}.blob.core.windows.net"
                self.blob_service_client = BlobServiceClient(account_url=account_url, credential=self.account_key)

            # Verificación de pre-condiciones: El contenedor destino debe existir
            self._ensure_container_exists()

        except Exception as e:
            logger.error(f"Error inicializando Azure Storage: {str(e)}")
            self.blob_service_client = None

    def _is_configured(self) -> bool:
        """
        Valida que existan las credenciales mínimas requeridas.
        
        Returns:
            bool: True si la configuración es válida, False en caso contrario.
        """
        return (
            (self.account_name and self.account_key) or
            self.connection_string
        ) and self.container_name

    def _ensure_container_exists(self):
        """
        Garantiza la existencia del contenedor (bucket) en el servicio remoto.
        Implementa una operación idempotente (safe creation).
        """        
        if not self.blob_service_client:
            return

        try:
            # Instanciación del cliente de nivel 'Contenedor'
            container_client = self.blob_service_client.get_container_client(self.container_name)
            # Intento de creación. Lanza ResourceExistsError si ya existe.
            container_client.create_container()
            logger.info(f"Contenedor '{self.container_name}' creado")

        except ResourceExistsError:
            # Manejo de excepción esperada: El recurso ya existe, flujo normal.
            logger.info(f"Contenedor '{self.container_name}' ya existe")
        except Exception as e:
            logger.error(f"Error creando contenedor: {str(e)}")

    def upload_file(self, file_obj: BinaryIO, blob_name: str, content_type: str = None) -> Optional[str]:
        """
        Realiza la transmisión (upload) de un flujo binario hacia Azure.

        Args:
            file_obj (BinaryIO): Objeto tipo archivo o buffer en memoria (debe soportar .read() y .seek()).
            blob_name (str): Identificador único (key) del objeto en el almacenamiento.
            content_type (str, optional): Tipo MIME del archivo (ej. 'image/jpeg').

        Returns:
            Optional[str]: URL absoluta del recurso creado, o None si la operación falla.
        """
        if not self.blob_service_client:
            logger.error("Azure Storage no está configurado")
            return None

        try:
            # Obtención del cliente de nivel 'Blob' (Objeto hoja en la jerarquía)
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            # CRÍTICO: Reinicio del puntero de lectura del stream.
            # Garantiza que se lea el archivo desde el byte 0, en caso de lecturas previas.
            file_obj.seek(0)  # Asegurar que estamos al inicio del archivo
            # Ejecución de la transferencia de datos. 'overwrite=True' impone semántica de reemplazo.
            blob_client.upload_blob(file_obj, overwrite=True, content_type=content_type)

            logger.info(f"Archivo '{blob_name}' subido exitosamente")
            return blob_client.url

        except Exception as e:
            logger.error(f"Error subiendo archivo '{blob_name}': {str(e)}")
            return None

    def download_file(self, blob_name: str) -> Optional[bytes]:
        """
        Descarga un archivo desde Azure Blob Storage

        Args:
            blob_name: Nombre del blob

        Returns:
            Contenido del archivo como bytes, None si falló
        """
        if not self.blob_service_client:
            logger.error("Azure Storage no está configurado")
            return None

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            download_stream = blob_client.download_blob()
            data = download_stream.readall()

            logger.info(f"Archivo '{blob_name}' descargado exitosamente")
            return data

        except ResourceNotFoundError:
            logger.error(f"Archivo '{blob_name}' no encontrado")
            return None
        except Exception as e:
            logger.error(f"Error descargando archivo '{blob_name}': {str(e)}")
            return None

    def delete_file(self, blob_name: str) -> bool:
        """
        Elimina un archivo de Azure Blob Storage

        Args:
            blob_name: Nombre del blob

        Returns:
            True si se eliminó correctamente, False si falló
        """
        if not self.blob_service_client:
            logger.error("Azure Storage no está configurado")
            return False

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )

            blob_client.delete_blob()
            logger.info(f"Archivo '{blob_name}' eliminado exitosamente")
            return True

        except ResourceNotFoundError:
            logger.warning(f"Archivo '{blob_name}' no encontrado para eliminar")
            return False
        except Exception as e:
            logger.error(f"Error eliminando archivo '{blob_name}': {str(e)}")
            return False

    def list_files(self, prefix: str = "") -> List[dict]:
        """
        Lista archivos en el contenedor

        Args:
            prefix: Prefijo para filtrar archivos

        Returns:
            Lista de diccionarios con información de los blobs
        """
        if not self.blob_service_client:
            logger.error("Azure Storage no está configurado")
            return []

        try:
            container_client = self.blob_service_client.get_container_client(self.container_name)
            blobs = container_client.list_blobs(name_starts_with=prefix)

            files = []
            for blob in blobs:
                files.append({
                    'name': blob.name,
                    'size': blob.size,
                    'last_modified': blob.last_modified,
                    'url': f"https://{self.account_name}.blob.core.windows.net/{self.container_name}/{blob.name}"
                })

            return files

        except Exception as e:
            logger.error(f"Error listando archivos: {str(e)}")
            return []

    def get_file_url(self, blob_name: str) -> Optional[str]:
        """
        Obtiene la URL de un archivo

        Args:
            blob_name: Nombre del blob

        Returns:
            URL del archivo, None si no existe
        """
        if not self.blob_service_client:
            return None

        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            return blob_client.url
        except Exception:
            return None

# Instanciación Singleton del servicio a nivel de módulo.
# Esto asegura que la conexión se configure una única vez al importar el módulo.
azure_storage = AzureStorageService()