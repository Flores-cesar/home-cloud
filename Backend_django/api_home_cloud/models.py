from django.db import models
from django.contrib.auth.models import User

# Familia (grupo familiar)
class Familia(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# PerfilUsuario (extiende el usuario de Django)
class PerfilUsuario(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('miembro', 'Miembro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='miembros')
    rol = models.CharField(max_length=20, choices=ROLES, default='miembro')

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


# Documento (archivos subidos)
class Documento(models.Model):
    TIPOS = [
        ('factura', 'Factura'),
        ('receta', 'Receta'),
        ('garantia', 'Garantía'),
        ('otro', 'Otro'),
    ]

    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='documentos')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documentos')
    nombre_archivo = models.CharField(max_length=255)
    url_archivo = models.URLField(max_length=500)
    tipo_documento = models.CharField(max_length=20, choices=TIPOS, default='otro')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    procesado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_archivo} - {self.tipo_documento}"


# Tarea (creada manualmente o por OCR)
class Tarea(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name='tareas')
    documento = models.ForeignKey(Documento, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tareas_creadas')
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"


# Notificación (para avisos automáticos)
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField(max_length=255)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notif. a {self.usuario.username}: {self.mensaje[:30]}..."