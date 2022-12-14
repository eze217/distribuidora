# Generated by Django 4.1 on 2022-10-20 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distribuidora_app', '0012_alter_pedidodetalleclientemodel_options_and_more'),
        ('user', '0002_remove_perfil_proveedor_perfil_cuenta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cuenta',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.cuentamodel'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='is_cliente',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='is_proveedor',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
