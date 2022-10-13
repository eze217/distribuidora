# Generated by Django 4.1 on 2022-09-21 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distribuidora_app', '0012_alter_pedidodetalleclientemodel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificacionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=100, verbose_name='Asunto')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripcion')),
                ('leida', models.BooleanField(default=False)),
                ('prioridad', models.CharField(choices=[('ALTA', 'ALTA'), ('MEDIA', 'MEDIA'), ('BAJA', 'BAJA')], max_length=10, verbose_name='Prioridad')),
                ('state', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('cuenta_notificada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.cuentamodel', verbose_name='Creo')),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creo')),
            ],
            options={
                'verbose_name': 'Notificacion',
                'verbose_name_plural': 'Notificaciones',
            },
        ),
    ]