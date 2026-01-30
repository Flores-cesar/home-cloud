# Generated manually for renaming Familia to Grupo

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_home_cloud', '0001_initial'),
    ]

    operations = [
        # Rename model Familia to Grupo
        migrations.RenameModel(
            old_name='Familia',
            new_name='Grupo',
        ),
        # Add new fields to Grupo model
        migrations.AddField(
            model_name='grupo',
            name='descripcion',
            field=models.TextField(blank=True, help_text='Descripción opcional del grupo'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='tipo_grupo',
            field=models.CharField(
                choices=[
                    ('familia', 'Familia'),
                    ('amigos', 'Grupo de Amigos'),
                    ('consorcio', 'Consorcio'),
                    ('equipo', 'Equipo de Trabajo'),
                    ('otro', 'Otro')
                ],
                default='familia',
                max_length=20
            ),
        ),
        # Rename foreign key fields
        migrations.RenameField(
            model_name='documento',
            old_name='familia',
            new_name='grupo',
        ),
        migrations.RenameField(
            model_name='perfilusuario',
            old_name='familia',
            new_name='grupo',
        ),
        migrations.RenameField(
            model_name='tarea',
            old_name='familia',
            new_name='grupo',
        ),
    ]