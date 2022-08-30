# Generated by Django 4.1 on 2022-08-30 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlmacenModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('address', models.CharField(max_length=200, verbose_name='Domicilio')),
                ('phone', models.CharField(max_length=15, verbose_name='Telefono')),
            ],
            options={
                'verbose_name': 'Almacen',
                'verbose_name_plural': 'Almacenes',
            },
        ),
        migrations.CreateModel(
            name='ProveedorModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('domicilio', models.CharField(max_length=200, verbose_name='Domicilio')),
                ('telefono', models.CharField(max_length=15, verbose_name='Telefono')),
                ('cif', models.CharField(max_length=20, verbose_name='CIF')),
                ('observaciones', models.CharField(blank=True, default='---', max_length=200, null=True, verbose_name='Notas')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProductoModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre producto')),
                ('precio', models.FloatField()),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.proveedormodel')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='PedidoModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('estado', models.CharField(choices=[('SOLICITADO', 'SOLICITADO'), ('CONFIRMADO', 'CONFIRMADO'), ('EN PREPARACION', 'EN PREPARACION'), ('ANULADO', 'ANULADO'), ('EN REPARTO', 'EN REPARTO'), ('ENTREGADO', 'ENTREGADO')], max_length=20, verbose_name='Estado ')),
                ('tipo_pedido', models.CharField(choices=[('COMPRA', 'COMPRA'), ('VENTA', 'VENTA')], max_length=10, verbose_name='Tipo de pedido')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.proveedormodel')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='PedidoDetalleModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('cantidad', models.IntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.pedidomodel')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.productomodel')),
            ],
            options={
                'verbose_name': 'Pedido detalle',
                'verbose_name_plural': 'Pedidos detalle',
            },
        ),
        migrations.CreateModel(
            name='AlmacenStockModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Fecha de modificación')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Fecha de eliminación')),
                ('cantidad', models.IntegerField()),
                ('movimiento', models.CharField(choices=[('INGRESO', 'INGRESO'), ('EGRESO', 'EGRESO')], max_length=10, verbose_name='Movimiento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribuidora_app.productomodel')),
            ],
            options={
                'verbose_name': 'Almacen Stock',
                'verbose_name_plural': 'Almacen Stock',
            },
        ),
    ]
